"""Steady heat loss of a whole kiln held at its top temperature.

Each face (left, right, back, front, floor, roof) is a layered wall solved on its own
(:mod:`kilndesigner.thermal.wall`), with its area growing through the lining
(:mod:`kilndesigner.shape`), and its outside losing heat to still air. The floor's underside is
treated as a hot plate facing down, as for a kiln standing on a stand.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner import cones
from kilndesigner.library import material
from kilndesigner.model import Face, Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.thermal.surface import StillAirSurface
from kilndesigner.thermal.wall import Slab, solve_wall
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

# CIBSE Guide C Table C3.7 (electric-and-thermal.md §4.7, [S52])
EMISSIVITY = {"painted": 0.95, "oxidised_steel": 0.79, "rolled_steel_sheet": 0.6}
EMISSIVITY_SOURCE = "CIBSE Guide C Table C3.7; electric-and-thermal.md §4.7 [S52]"
METHOD_SOURCE = (
    "Layered wall with k(T), iterated surface temperature, as ASTM C680; natural convection by "
    "Churchill–Chu and Lloyd–Moran; electric-and-thermal.md §6"
)


class LayerResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    material: str
    thickness: str
    hot_side: str
    cold_side: str


class FaceResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    face: Face
    inside_area: str
    outside_area: str
    heat_loss: str
    surface_temperature: str
    layers: list[LayerResult]


class HeatLoss(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    top_temperature: str
    ambient: str
    total: str
    total_watts: float
    faces: list[FaceResult]
    working: list[Step]
    findings: list[Finding]


def top_temperature(kiln: Kiln) -> tuple[Quantity, Step]:
    firing = kiln.firing
    if firing.top_temperature is not None:
        t = firing.top_temperature
        return t, Step(name="Top temperature", value=show(t), note="as given in the design")
    assert firing.cone is not None
    t = cones.cone_temperature(firing.cone, firing.final_rate)
    return t, Step(
        name="Top temperature",
        value=f"{show(t, 'degC')} ({show(t, 'degF')})",
        inputs={"cone": firing.cone, "final heating rate": f"{firing.final_rate} °C/h"},
        reference=cones.CONE_SOURCE,
    )


def heat_loss(
    kiln: Kiln, *, ambient: Quantity | None = None, inside: Quantity | None = None
) -> HeatLoss:
    """Heat loss with the inside held at the top temperature (or ``inside``), in still air."""
    top, top_step = top_temperature(kiln)
    if inside is not None:
        top, top_step = inside, Step(name="Inside temperature", value=show(inside))
    air = ambient if ambient is not None else kiln.site.ambient
    t_in, t_air = si(top, "K"), si(air, "K")
    emissivity = EMISSIVITY[kiln.shell.finish]
    units = "us" if kiln.units == "us" else "metric"
    temp_unit, area_unit, len_unit = (
        ("degF", "ft**2", "in") if units == "us" else ("degC", "m**2", "mm")
    )

    working: list[Step] = [
        top_step,
        Step(name="Air around the kiln", value=show(air, temp_unit)),
        Step(
            name="Shell emissivity",
            value=show(emissivity),
            inputs={"finish": kiln.shell.finish},
            reference=EMISSIVITY_SOURCE,
        ),
    ]
    findings: list[Finding] = []
    faces: list[FaceResult] = []
    total = 0.0
    excerpt_materials: set[str] = set()

    for shape in chamber_shape(kiln).faces():
        layers = kiln.lining.for_face(shape.face, door_face=kiln.door_face)
        slabs: list[Slab] = []
        for layer in layers:
            m = material(layer.material)
            if m.status == "excerpt":
                excerpt_materials.add(m.name)
            slabs.append(Slab(m.id, si(layer.thickness, "m"), m.k))
        thickness = sum(s.thickness for s in slabs)
        surface = StillAirSurface(
            shape.orientation, shape.characteristic_length(thickness), emissivity
        )
        result = solve_wall(slabs, t_in, t_air, surface, area=shape.area_at)
        total += result.heat_flow

        temps = result.temperatures
        layer_results: list[LayerResult] = []
        for i, layer in enumerate(layers):
            m = material(layer.material)
            hot = Q_(temps[i], "K")
            limit = m.max_service_temperature
            if si(hot, "K") > si(limit, "K") + 1e-6:
                findings.append(
                    Finding(
                        level="error",
                        message=(
                            f"{shape.face}: {m.name} would run at {show(hot, temp_unit)} on its "
                            f"hot side, above its {show(limit, temp_unit)} limit. Use a "
                            f"higher-rated material or move it further out."
                        ),
                        reference=m.source,
                    )
                )
            layer_results.append(
                LayerResult(
                    material=m.id,
                    thickness=show(layer.thickness, len_unit),
                    hot_side=show(hot, temp_unit),
                    cold_side=show(Q_(temps[i + 1], "K"), temp_unit),
                )
            )
        faces.append(
            FaceResult(
                face=shape.face,
                inside_area=show(Q_(shape.inside_area, "m**2"), area_unit),
                outside_area=show(Q_(result.outside_area, "m**2"), area_unit),
                heat_loss=show(Q_(result.heat_flow, "W"), "W"),
                surface_temperature=show(Q_(result.surface, "K"), temp_unit),
                layers=layer_results,
            )
        )
        working.append(
            Step(
                name=f"Heat loss, {shape.face}",
                value=show(Q_(result.heat_flow, "W"), "W"),
                formula="Q = A_out·h(Ts)·(Ts − T∞); ∫k dT across each layer = Q·∫dx/A(x)",
                inputs={
                    "outside surface": show(Q_(result.surface, "K"), temp_unit),
                    "surface coefficient h": show(
                        Q_(result.surface_coefficient, "W/(m**2*K)"), "W/(m**2*K)"
                    ),
                    "outside area": show(Q_(result.outside_area, "m**2"), area_unit),
                },
                reference=METHOD_SOURCE,
            )
        )

    total_q = Q_(total, "W")
    working.append(
        Step(
            name="Total heat loss at top temperature",
            value=f"{show(total_q, 'kW')} ({show(total_q, 'BTU/hr', 3)})",
            formula="sum of the six faces",
        )
    )
    if excerpt_materials:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Some material data comes from extracts of the makers' data sheets and should "
                    "be checked against the sheets themselves: "
                    + ", ".join(sorted(excerpt_materials))
                ),
            )
        )
    findings.append(
        Finding(
            level="info",
            message=(
                "Heat loss is the steady loss with the kiln held at top temperature. It does not "
                "include the heat stored in the walls and ware during the firing."
            ),
        )
    )
    return HeatLoss(
        top_temperature=show(top, temp_unit),
        ambient=show(air, temp_unit),
        total=show(total_q, "kW"),
        total_watts=total,
        faces=faces,
        working=working,
        findings=findings,
    )
