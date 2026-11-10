"""v2's rays (`heat/rays.py`, `heat/chamber.py`): Monte Carlo view factors and grey-gas exchange
areas on trimesh + Embree, closed by Larsen & Howell's smoothing; checked against `radiation.py`'s
exact factors, a sphere's closed form, Cauchy's mean chord and a half shadow, then on the engine's
own chamber solids."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import trimesh  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.designfile import load_design
from kilndesigner.shape import Arch
from kilndesigner.thermal.radiation import BOX_FACES, box, covered
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import rays

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
IN = 0.0254
N = 100_000


def _cube_zones() -> list[rays.Zone]:
    """A unit cube from build123d, its faces named as `radiation.box` names them."""
    from build123d import Box, Pos

    def name(face: Any) -> str:
        c = face.center()
        for axis, (lo, hi) in (("X", ("left", "right")), ("Y", ("front", "back")),
                               ("Z", ("floor", "roof"))):  # fmt: skip
            v = getattr(c, axis) - (0.5 if axis == "Z" else 0.0)
            if abs(abs(v) - 0.5) < 1e-9:
                return lo if v < 0 else hi
        raise AssertionError(c)

    return rays.solid_zones(Pos(0, 0, 0.5) * Box(1, 1, 1), name, tol=0.01, scale=1.0)


@pytest.fixture(scope="module")
def cube() -> rays.Rays:
    zones = sorted(_cube_zones(), key=lambda z: BOX_FACES.index(z.name))
    return rays.trace(zones, rays=N, volume=1.0)


def test_embree_traces_the_rays() -> None:
    mesh: Any = trimesh.creation.box()
    assert type(mesh.ray).__module__ == "trimesh.ray.ray_pyembree"


def test_the_cubes_factors_match_the_exact_ones(cube: rays.Rays) -> None:
    """Howell C-11 and C-14 (`radiation.box`): within 3e-3 at 10⁵ rays a face (1/√N noise), and
    the closure makes summation and reciprocity exact."""
    exact = box(1, 1, 1).view
    assert np.abs(cube.raw - exact).max() < 3e-3
    closed = cube.view()  # radiation.Enclosure refuses anything not closed to 1e-9
    assert np.abs(closed.view - exact).max() < 3e-3
    assert cube.lost == 0


def test_cauchys_mean_chord_is_4v_over_a(cube: rays.Rays) -> None:
    """In the thin-gas limit Σ g s_i = 4kV (Cauchy: Σ A_i·mean chord_i = 4V; Lienhard Table
    10.4's L₀ = 2ℓ/3 for a cube)."""
    k = 1e-3
    _, gs = cube.exchange(k)
    assert gs.sum() == pytest.approx(4 * k * 1.0, rel=5e-3)
    traced = rays.trace(_cube_zones(), rays=N)  # the volume from the rays' chords
    assert traced.volume == pytest.approx(1.0, rel=5e-3)


def test_the_closure_is_exact_for_a_grey_gas(cube: rays.Rays) -> None:
    for k in (0.0, 0.3, 3.0):
        ss, gs = cube.exchange(k)
        assert np.abs(ss - ss.T).max() < 1e-14
        assert np.abs(ss.sum(axis=1) + gs - cube.areas).max() < 1e-12
        assert ss.min() >= 0
        assert gs.min() >= 0


@pytest.mark.parametrize("kd", [0.1, 1.0, 3.0])
def test_a_spheres_gas_absorptance(kd: float) -> None:
    """A grey gas in a sphere of diameter D absorbs ε = 1 − 2[1 − (1 + a)e^(−a)]/a² of the wall's
    diffuse emission, a = kD (a chord at θ to the normal is D cos θ; Derived)."""
    s: Any = trimesh.creation.icosphere(subdivisions=4, radius=0.5)
    wall = rays.Zone("wall", np.asarray(s.triangles)[:, [0, 2, 1]])
    r = rays.trace([wall], rays=N)
    _, gs = r.exchange(kd)
    eps = 1 - 2 * (1 - (1 + kd) * math.exp(-kd)) / kd**2
    assert gs[0] / r.areas[0] == pytest.approx(eps, abs=4e-3)


def test_a_half_shadow() -> None:
    """Two coaxial unit squares 1 m apart, a blocker just in front of half the receiver: by
    symmetry half the unobstructed factor (Howell C-11's 0.19982)."""

    def square(x0: float, x1: float, z: float, up: bool) -> rays.Zone:
        v = np.array([[x0, -0.5, z], [x1, -0.5, z], [x1, 0.5, z], [x0, 0.5, z]])
        f = [[0, 1, 2], [0, 2, 3]] if up else [[0, 2, 1], [0, 3, 2]]
        return rays.Zone(f"sq{z}{x0}", v[np.array(f)])

    emitter, receiver = square(-0.5, 0.5, 0.0, True), square(-0.5, 0.5, 1.0, False)
    blocker = square(-0.5, 0.0, 0.999, False)
    for zones, want in (([emitter, receiver], 0.19982), ([emitter, receiver, blocker], 0.09991)):
        r = rays.trace(zones, rays=200_000, closed=False)
        assert r.raw[0, 1] == pytest.approx(want, abs=3.5e-3)
        assert r.lost > 0
    with pytest.raises(rays.GeometryError, match="escaped"):
        rays.trace([emitter, receiver], rays=1000)


@pytest.mark.geometry
def test_the_engines_sprung_arch_against_the_covered_formula() -> None:
    """The fast-fire's gas volume as `massing._cavity` draws it, the end walls' segments over the
    springline counted with the crown: against `radiation.covered` (Lienhard Exs. 10.1, 10.3) with
    the mesh's own crown area."""
    from build123d import Compound, Keep, Plane

    from kilndesigner.massing import _cavity, cells, run_of  # pyright: ignore[reportPrivateUsage]

    kiln = load_design(OLSEN / "fast-fire.yaml")
    _, volume, (w, d, h) = ch.cavity(kiln)
    run = run_of(kiln)
    (cell,) = [c for c in cells(kiln, run) if c.kind == "box"]
    cut = _cavity(kiln, run, cell, 0.0).split(Plane.XY.offset(h * 1e3), keep=Keep.ALL)
    walls = ch._classify(w * 1e3, d * 1e3)  # pyright: ignore[reportPrivateUsage]

    def name(face: Any) -> str | None:
        c = face.center()
        if abs(c.Z - h * 1e3) < 1e-3 and face.geom_type.name == "PLANE":
            return None  # the cut at the springline
        return "roof" if h * 1e3 < c.Z else walls(face)

    crown = rays.solid_zones(Compound(children=list(cut)), name)
    crown.sort(key=lambda z: BOX_FACES.index(z.name))
    r = rays.trace(crown, rays=N, volume=volume)
    arch = Arch(w, si_rise(kiln))
    exact_crown = arch.arc_length * d + 2 * arch.segment_area
    assert r.areas[BOX_FACES.index("roof")] == pytest.approx(exact_crown, rel=2e-3)
    exact = covered(box(w, d, h), "roof", float(r.areas[BOX_FACES.index("roof")])).view
    assert np.abs(r.view().view - exact).max() < 4e-3
    assert volume == pytest.approx(w * d * h + arch.segment_area * d, rel=1e-6)


def si_rise(kiln: Any) -> float:
    return kiln.roof.rise.to("m").magnitude


@pytest.mark.geometry
def test_the_fast_fires_own_chamber_with_its_openings_and_setting() -> None:
    """The engine's chamber: the walls, the floor with the two inlet flues of its S plan (the
    engine's layout), the 9 × 7½ in exit flue at the back and the 2½ in spy hole in the door, and
    a setting (test envelope) in the way. Closed; a symmetric chamber reads symmetric."""
    kiln = load_design(OLSEN / "fast-fire.yaml")
    c = ch.chamber(kiln)
    names = [p.name for p in c.patches]
    assert names == ["exit flue", "inlet flue 1", "inlet flue 2", "spy hole 1"]
    inlets = [p for p in c.patches if p.name.startswith("inlet")]
    assert [round(p.area / IN**2, 2) for p in inlets] == [60.75, 60.75]
    xs = sorted(p.centre[0] for p in inlets)
    assert xs[0] < 0 < xs[1]  # one each side: the S
    setting = rays.box_zone("setting", (-9 * IN, -9 * IN, 9 * IN), (9 * IN, 12.5 * IN, 33 * IN))
    vol = c.volume - rays.box_volume((-9 * IN, -9 * IN, 9 * IN), (9 * IN, 12.5 * IN, 33 * IN))
    r = rays.trace([*c.zones, setting], c.patches, rays=50_000, volume=vol)
    assert r.lost == 0
    e = r.view()
    a = {n: float(x) for n, x in zip(r.names, r.areas, strict=True)}
    assert a["exit flue"] == pytest.approx(67.5 * IN**2)
    wall = 27 * 36 * IN**2 + Arch(27 * IN, 3.375 * IN).segment_area
    assert a["back"] == pytest.approx(wall - 67.5 * IN**2, rel=2e-3)
    assert a["front"] == pytest.approx(wall - 6.25 * IN**2, rel=2e-3)
    left, right = e.factor("left", "setting"), e.factor("right", "setting")
    assert left == pytest.approx(right, abs=0.01)
    # The closure moves the factors by the noise only, the 2½ in spy hole's row included (a
    # plain average of the two directions moved it 0.011 at 2×10⁵ rays: Loehrke's weighting)
    assert np.abs(e.view - r.raw).max() < 0.006
    assert r.steps[0].name.startswith("Radiation between faces")


@pytest.mark.geometry
def test_chambers_v2_doesnt_take_yet_are_refused() -> None:
    with pytest.raises(ch.NotModelledError, match="one straight box"):
        ch.cavity(load_design(OLSEN / "olsen-two-chamber.yaml"))


def _design(name: str, change: dict[str, Any]) -> Any:
    import yaml

    from kilndesigner.model import Kiln

    data = yaml.safe_load((OLSEN / f"{name}.yaml").read_text(encoding="utf-8"))
    for key, value in change.items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


def _hole(wall: str, across: str = "0 in", up: str | None = "20 in") -> dict[str, Any]:
    h: dict[str, Any] = {"port": {"width": "2 in", "height": "3 in"}, "wall": wall,
                         "across": across}  # fmt: skip
    if up is not None:
        h["up"] = up
    return h


DIMS = (1.0, 2.0, 1.5)


@pytest.mark.parametrize("wall", ["front", "back", "left", "right"])
def test_a_hole_on_each_wall_lies_on_its_plane_facing_the_gas(wall: str) -> None:
    p = ch.wall_patch("h", wall, (0.2, 0.1), 0.3, 0.5, DIMS)
    c = np.asarray(p.centre)
    inward = {"front": (0, 1, 0), "back": (0, -1, 0), "left": (1, 0, 0), "right": (-1, 0, 0)}
    assert np.allclose(p.normal, inward[wall])
    assert c[2] == pytest.approx(0.5)
    # to the right seen from outside: front +x, back −x, left −y, right +y
    right = {"front": (0.3, -1.0), "back": (-0.3, 1.0), "left": (-0.5, -0.3), "right": (0.5, 0.3)}
    assert tuple(c[:2]) == pytest.approx(right[wall])
    assert p.area == pytest.approx(0.02)
    with pytest.raises(ch.NotModelledError, match="isn't placed"):
        ch.wall_patch("h", "roof", (0.2, 0.1), 0.0, 0.5, DIMS)


@pytest.mark.geometry
def test_a_burner_kilns_openings() -> None:
    """The 36 ft³ cross-draft with a round flue, six 3 in round burner ports and spy holes in
    three walls and the roof (test inputs; its design gives none of them)."""
    k = _design(
        "olsen-crossdraft-36",
        {
            "draft.flue_port": {"diameter": "6 in"},
            "heat.gas.burners.port": {"diameter": "3 in"},
            "spy_holes": {"holes": [_hole("back"), _hole("left", "4 in"), _hole("right"),
                                    _hole("roof", up=None)]},
        },
    )  # fmt: skip
    c = ch.chamber(k)
    names = [p.name for p in c.patches]
    assert names[:7] == ["exit flue", *(f"burner port {i}" for i in range(1, 7))]
    assert names[7:] == ["spy hole 1", "spy hole 2", "spy hole 3"]
    assert c.patches[0].area == pytest.approx(math.pi * (6 * IN) ** 2 / 4)
    assert c.patches[1].centre[2] == pytest.approx(2.5 * IN + math.sqrt(math.pi / 4) * 1.5 * IN)
    notes = " ".join(c.notes)
    assert "square of its area" in notes
    assert "spread evenly" in notes
    assert "in the roof" in notes
    r = rays.trace(list(c.zones), c.patches, rays=5_000, volume=c.volume)
    assert r.index("burner port 6") == len(c.zones) + 6
    unknown = ch.openings(_design("olsen-crossdraft-36", {}), DIMS)[1]
    assert "size isn't given" in " ".join(unknown)


def test_openings_that_fit_stay_where_the_layout_puts_them() -> None:
    """Narrower fireboxes whose inlets lie on the floor aren't moved; rectangular burner ports
    keep their sides."""
    narrow = _design(
        "fast-fire",
        {"heat.fire.fireboxes": [{"count": 2, "position": "under", "width": "9 in",
                                  "length": "40.5 in", "height": "6 in",
                                  "inlet": {"width": "9 in", "height": "4.5 in"}}]},
    )  # fmt: skip
    patches, notes = ch.openings(narrow, (27 * IN, 27 * IN, 36 * IN))
    assert [p.name for p in patches][1:3] == ["inlet flue 1", "inlet flue 2"]
    assert not any("moved onto the floor" in n for n in notes)
    square = _design(
        "olsen-crossdraft-36", {"heat.gas.burners.port": {"width": "3 in", "height": "4 in"}}
    )
    ports, _ = ch.openings(square, DIMS)
    assert ports[0].half == pytest.approx((2 * IN, 1.5 * IN))


@pytest.mark.geometry
def test_a_flat_roof_is_the_roof() -> None:
    k = _design("olsen-crossdraft-36", {"roof": {"type": "flat"}})
    zones, volume, (w, d, h) = ch.cavity(k)
    assert sorted(z.name for z in zones) == sorted(BOX_FACES)
    assert volume == pytest.approx(w * d * h, rel=1e-9)


def test_several_exit_flues_are_refused() -> None:
    exits = [{"through": "back", "count": 2, "port": {"width": "4.5 in", "height": "9 in"}}]
    k = _design("fast-fire", {"draft.flue_port": None, "draft.exits": exits})
    with pytest.raises(ch.NotModelledError, match="several exit flues"):
        ch.openings(k, DIMS)


def test_the_closure_refuses_a_negative_exchange_area() -> None:
    x = np.array([[0.5, 0.5], [0.5, 0.5]])
    with pytest.raises(rays.GeometryError, match="negative"):
        rays.smooth(np.array([0.4, 1.0]), x, np.eye(2))


def test_a_triangle_with_no_area_is_refused() -> None:
    flat = rays.Zone("flat", np.zeros((1, 3, 3)))
    with pytest.raises(rays.GeometryError, match="no area"):
        rays.trace([flat], rays=10)


def test_an_opening_off_its_face_is_refused() -> None:
    z = _cube_zones()
    off = rays.Patch("hole", "floor", (0.45, 0.0, 0.0), (1, 0, 0), (0, 1, 0), (0.1, 0.1))
    with pytest.raises(rays.GeometryError, match="wholly on its face"):
        rays.trace(z, [off], rays=100)
    nowhere = rays.Patch("hole", "door", (0.0, 0.0, 0.0), (1, 0, 0), (0, 1, 0), (0.1, 0.1))
    with pytest.raises(rays.GeometryError, match="not a zone"):
        rays.trace(z, [nowhere], rays=100)


def test_an_opening_carved_from_a_face() -> None:
    """A 0.2 m square hole in the cube's floor: its own zone, the floor's area less it, and from
    the floor's middle it sees more of the roof than the floor does on average (0.19982)."""
    hole = rays.Patch("hole", "floor", (0.0, 0.0, 0.0), (1, 0, 0), (0, 1, 0), (0.1, 0.1))
    r = rays.trace(_cube_zones(), [hole], rays=N)
    a = dict(zip(r.names, r.areas, strict=True))
    assert a["floor"] == pytest.approx(1.0 - 0.04)
    assert a["hole"] == pytest.approx(0.04)
    f = r.view()
    assert f.factor("hole", "roof") > 0.21
    assert f.factor("floor", "roof") == pytest.approx(0.1998, abs=4e-3)
