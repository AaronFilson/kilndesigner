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
    whole = ch.cavity(kiln)
    volume, w, h = whole.volume, whole.width, whole.height
    run = run_of(kiln)
    (cell,) = [c for c in cells(kiln, run) if c.kind == "box"]
    cut = _cavity(kiln, run, cell, 0.0).split(Plane.XY.offset(h * 1e3), keep=Keep.ALL)

    def name(face: Any) -> str | None:
        c = face.center()
        if abs(c.Z - h * 1e3) < 1e-3 and face.geom_type.name == "PLANE":
            return None  # the cut at the springline
        if h * 1e3 < c.Z:
            return "roof"
        if abs(c.Z) < 1e-3:
            return "floor"
        if abs(face.normal_at(c).Y) > 0.999:
            return "front" if c.Y < 0 else "back"
        return "left" if c.X < 0 else "right"

    crown = rays.solid_zones(Compound(children=list(cut)), name)
    crown.sort(key=lambda z: BOX_FACES.index(z.name))
    r = rays.trace(crown, rays=N, volume=volume)
    d = whole.depth
    arch = Arch(w, si_rise(kiln))
    exact_crown = arch.arc_length * d + 2 * arch.segment_area
    assert r.areas[BOX_FACES.index("roof")] == pytest.approx(exact_crown, rel=2e-3)
    exact = covered(box(w, d, h), "roof", float(r.areas[BOX_FACES.index("roof")])).view
    assert np.abs(r.view().view - exact).max() < 4e-3
    assert volume == pytest.approx(w * d * h + arch.segment_area * d, rel=1e-6)
    # The chamber's own naming: the end walls' segments over the springline with their walls
    a = {z.name: rays.trace([z], rays=10, closed=False).areas[0] for z in whole.zones}
    assert a["roof"] == pytest.approx(arch.arc_length * d, rel=2e-3)
    assert a["back"] == pytest.approx(w * h + arch.segment_area, rel=2e-3)


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
    # 4½ in along each firebox × the 11¼ in of its 13½ in width the 27 in floor exposes
    assert [round(p.area / IN**2, 2) for p in inlets] == [50.62, 50.62]
    assert not any("moved onto the floor" in n for n in c.notes)
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
def test_what_the_chamber_still_refuses() -> None:
    bent = _design("anagama-hole", {"chamber.bend": "30 degree"})
    with pytest.raises(ch.NotModelledError, match="bent run"):
        ch.cavity(bent)
    with pytest.raises(ch.NotModelledError, match="chambers in a row are zones"):
        ch.cavity(load_design(OLSEN / "olsen-two-chamber.yaml"), segments=2)
    with pytest.raises(ch.NotModelledError, match="one segment or more"):
        ch.cavity(load_design(OLSEN / "anagama-hole.yaml"), segments=0)


def _areas(c: ch.Chamber) -> dict[str, float]:
    out: dict[str, float] = {}
    for z in c.zones:
        t = z.triangles
        out[z.name] = float(0.5 * np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]),
                                                 axis=1).sum())  # fmt: skip
    return out


def _cylinder(names: tuple[str, ...], r: float, h: float) -> Any:
    """A closed cylinder's exact factors: floor to roof by coaxial discs (Lienhard Table 10.3
    case 3), the rest by summation and reciprocity."""
    from kilndesigner.thermal.radiation import Enclosure, coaxial_discs

    disc, side = math.pi * r * r, 2 * math.pi * r * h
    f_fr = coaxial_discs(r, r, h)
    f_ws = disc * (1 - f_fr) / side
    f = {("floor", "roof"): f_fr, ("floor", "wall"): 1 - f_fr, ("roof", "floor"): f_fr,
         ("roof", "wall"): 1 - f_fr, ("wall", "floor"): f_ws, ("wall", "roof"): f_ws,
         ("wall", "wall"): 1 - 2 * f_ws}  # fmt: skip
    view = np.array([[f.get((a, b), 0.0) for b in names] for a in names])
    areas = tuple({"floor": disc, "roof": disc, "wall": side}[n] for n in names)
    return Enclosure(names, areas, view)


@pytest.mark.geometry
def test_a_round_chamber_against_coaxial_discs() -> None:
    """A round chamber under a flat roof (`round-electric`): its floor sees its roof as two
    coaxial discs do, the wall the rest; its areas and volume the cylinder's."""
    c = ch.chamber(load_design(ROOT / "examples" / "round-electric.yaml"))
    assert c.shape == "round"
    r_, h = c.width / 2, c.height
    a = _areas(c)
    assert a["floor"] == pytest.approx(math.pi * r_**2, rel=3e-3)
    assert a["wall"] == pytest.approx(2 * math.pi * r_ * h, rel=3e-3)
    assert c.volume == pytest.approx(math.pi * r_**2 * h, rel=3e-3)
    traced = rays.trace(list(c.zones), rays=N, volume=c.volume)
    exact = _cylinder(traced.names, r_, h)
    assert np.abs(traced.view().view - exact.view).max() < 6e-3


@pytest.mark.geometry
def test_a_dome_over_a_round_chamber_against_the_covered_formula() -> None:
    """Breda's bottle kiln: the dome a spherical cap of area π(a² + rise²) over the cylinder's
    top, its factors as `radiation.covered` gives them (Lienhard Exs. 10.1, 10.3). Its exits
    through the dome aren't carved (said)."""
    k = load_design(OLSEN / "breda-bottle.yaml")
    c = ch.chamber(k)
    assert any("curved roof" in n for n in c.notes)
    r_, h, rise = c.width / 2, c.height, si_rise(k)
    cap = math.pi * (r_**2 + rise**2)
    assert _areas(c)["roof"] == pytest.approx(cap, rel=3e-3)
    traced = rays.trace(list(c.zones), rays=N, volume=c.volume)
    dome = float(traced.areas[traced.index("roof")])
    exact = covered(_cylinder(traced.names, r_, h), "roof", dome)
    assert np.abs(traced.view().view - exact.view).max() < 6e-3


@pytest.mark.geometry
def test_an_open_top_is_its_own_face() -> None:
    c = ch.chamber(load_design(OLSEN / "kenzan-muffle.yaml"))
    assert sorted(z.name for z in c.zones) == ["floor", "open top", "wall"]
    a = _areas(c)
    assert a["open top"] == pytest.approx(a["floor"], rel=1e-3)


@pytest.mark.geometry
def test_a_sail_dome_and_a_catenary() -> None:
    """A box under a sail dome (`dome-castable-kiln`): the dome's area and each wall's segment
    over the springline as `shape.SailDome` gives them; a catenary (Ward's parabola,
    `catenary-gas-kiln`): its vault's area the parabola's length times the depth. Each closed:
    Cauchy's volume from the rays within 0.5 % of the solid's."""
    from kilndesigner.shape import SailDome

    k = load_design(ROOT / "examples" / "dome-castable-kiln.yaml")
    c = ch.chamber(k)
    w, d, h = c.width, c.depth, c.height
    dome = SailDome(w, d, si_rise(k))
    a = _areas(c)
    assert a["roof"] == pytest.approx(dome.area(), rel=3e-3)
    assert a["left"] == pytest.approx(d * h + dome.segment(w / 2, d), rel=3e-3)
    assert a["front"] == pytest.approx(w * h + dome.segment(d / 2, w), rel=3e-3)
    traced = rays.trace(list(c.zones), rays=50_000)
    assert traced.volume == pytest.approx(c.volume, rel=5e-3)
    k = load_design(ROOT / "examples" / "catenary-gas-kiln.yaml")
    c = ch.chamber(k)
    assert sorted(z.name for z in c.zones) == ["back", "floor", "front", "roof"]
    half, top = c.width / 2, c.height
    xs = half * (2 * np.arange(25) / 24 - 1)
    curve = np.column_stack([xs, top * (1 - (xs / half) ** 2)])
    length = float(np.linalg.norm(np.diff(curve, axis=0), axis=1).sum())
    assert _areas(c)["roof"] == pytest.approx(length * c.depth, rel=2e-3)
    traced = rays.trace(list(c.zones), rays=50_000)
    assert traced.volume == pytest.approx(c.volume, rel=5e-3)


@pytest.mark.geometry
def test_chambers_in_a_row_are_gas_zones() -> None:
    """Olsen's two-chamber kiln: each chamber a gas zone, joined through the flue holes in the
    wall between them; that wall's two faces and the holes' sides built in it; each zone's
    volume from its own chords within 1 %; Hottel's rows; each chamber's floor sees its own gas
    more than the other's."""
    c = ch.chamber(load_design(OLSEN / "olsen-two-chamber.yaml"))
    assert [g.name for g in c.gas] == ["chamber 1", "chamber 2"]
    names = {z.name for z in c.zones}
    assert {"back 1", "front 2", "flues 1", "flues 2", "front 1", "back 2"} <= names
    assert c.built["back 1"] == ("between", 0)
    assert c.built["front 2"] == ("between", 1)
    assert c.built["flues 2"] == ("between", 1)
    assert c.built["front 1"] == ("front", 0)
    assert c.built["roof 2"] == ("roof", 1)
    assert len(c.rooms) == 2
    k = 0.5
    r = rays.trace(list(c.zones), c.patches, rays=30_000, regions=c.regions(),
                   gas=[g.name for g in c.gas], ks=(k,))  # fmt: skip
    assert r.gas_volumes == pytest.approx([g.volume for g in c.gas], rel=1e-2)
    ss, gs, gg = r.exchange_zones(k)
    assert np.abs(ss.sum(axis=1) + gs.sum(axis=0) - r.areas).max() < 1e-12
    assert gs.sum(axis=1) + gg.sum(axis=1) == pytest.approx(4 * k * r.gas_volumes, rel=1e-2)
    f1, f2 = r.index("floor 1"), r.index("floor 2")
    assert gs[0, f1] > 5 * gs[1, f1]
    assert gs[1, f2] > 5 * gs[0, f2]


@pytest.mark.geometry
def test_a_tube_cut_into_segments() -> None:
    """The anagama in a hole cut into four segments: four gas zones of a quarter of the volume
    each, each wall split at the cuts (a quarter of the whole each), the front wall in the first
    and the back in the last; the regions tile every ray's path."""
    k = load_design(OLSEN / "anagama-hole.yaml")
    whole = _areas(ch.cavity(k))
    c = ch.cavity(k, segments=4)
    assert len(c.gas) == 4
    assert [g.volume for g in c.gas] == pytest.approx([c.volume / 4] * 4, rel=1e-6)
    a = _areas(c)
    assert sum(a[f"left {i}"] for i in range(1, 5)) == pytest.approx(whole["left"], rel=1e-6)
    assert a["left 2"] == pytest.approx(whole["left"] / 4, rel=1e-6)
    assert "front 1" in a
    assert "back 4" in a
    assert "front 2" not in a
    r = rays.trace(list(c.zones), rays=10_000, regions=c.regions(),
                   gas=[g.name for g in c.gas], ks=(0.3,))  # fmt: skip
    assert r.gas_volumes == pytest.approx([c.volume / 4] * 4, rel=2e-2)


@pytest.mark.geometry
def test_the_fast_fires_whole_gas_path_as_one_enclosure() -> None:
    """H13: the fireboxes (from the grate up, their inlet flues through the floor) and the chimney
    (its channel through the back wall and its stack) as gas zones of the chamber's enclosure:
    the floor's underside the fireboxes' roof, the grate the fire; each zone's volume by its own
    chords (Cauchy) within 1 %; the inlet and exit flues no longer openings."""
    c = ch.chamber(load_design(OLSEN / "fast-fire.yaml"), path=True)
    assert [(g.name, g.kind) for g in c.gas] == [
        ("firebox", "firebox"), ("chamber", "chamber"), ("chimney", "chimney"),
    ]  # fmt: skip
    a = _areas(c)
    assert {"grate", "firebox walls", "firebox roof", "inlet flues", "exit flue",
            "chimney walls", "chimney top"} <= set(a)  # fmt: skip
    assert a["grate"] == pytest.approx(2 * 13.5 * 40.5 * IN**2, rel=1e-6)
    assert a["chimney top"] == pytest.approx(81 * IN**2, rel=1e-6)
    assert c.built["firebox roof"] == ("floor", 0)
    assert c.built["firebox walls"] == ("firebox", 0)
    assert c.built["chimney walls"] == ("chimney", 2)
    assert c.built["floor"] == ("floor", 1)
    assert [p.name for p in c.patches] == ["spy hole 1"]
    stack = 9 * 9 * IN**2 * (14 * 12 * IN + 4.5 * IN)
    assert c.gas[2].volume == pytest.approx(stack + 9 * 7.5 * 9 * IN**3, rel=1e-6)
    r = rays.trace(list(c.zones), c.patches, rays=20_000, regions=c.regions(),
                   gas=[g.name for g in c.gas], ks=(0.5,))  # fmt: skip
    assert r.lost == 0
    assert r.gas_volumes == pytest.approx([g.volume for g in c.gas], rel=1e-2)


@pytest.mark.geometry
def test_crossing_gas_paths() -> None:
    """The Fireworks kiln: two tubes crossing at right angles over one fire zone, their vaults
    meeting in a groin: one gas zone, its floor the 9 × 9 ft plan, its volume the crossing's
    (`groin.CrossingShape`) and from the rays' chords."""
    from kilndesigner.groin import CrossingShape, tubes

    k = load_design(OLSEN / "fireworks-edmonton.yaml")
    c = ch.chamber(k)
    assert c.shape == "crossing"
    assert len(c.gas) == 1
    assert _areas(c)["floor"] == pytest.approx((9 * 12 * IN) ** 2, rel=1e-6)
    assert c.volume == pytest.approx(CrossingShape(tubes(k, "m")).volume(), rel=5e-3)
    traced = rays.trace(list(c.zones), rays=50_000)
    assert traced.volume == pytest.approx(c.volume, rel=5e-3)


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
    c = ch.cavity(_design("olsen-crossdraft-36", {"roof": {"type": "flat"}}))
    assert sorted(z.name for z in c.zones) == sorted(BOX_FACES)
    assert c.volume == pytest.approx(c.width * c.depth * c.height, rel=1e-9)


@pytest.mark.geometry
def test_openings_on_the_shapes_faces() -> None:
    """Exit holes (`draft.exits`) where the engine cuts them, slid onto their face when the
    layout puts them past its edge; a firebox's inlets through its wall; openings with no flat
    face to go on (a catenary's side, a round wall) left out; each said."""
    c = ch.chamber(load_design(OLSEN / "kahler-salt.yaml"))
    exits = [p for p in c.patches if p.name.startswith("exit flue")]
    assert exits
    assert {p.face for p in exits} == {"floor"}
    assert any("onto its face" in n for n in c.notes)
    sturt = ch.chamber(load_design(OLSEN / "blakebrough-sturt.yaml"))
    assert not sturt.patches
    assert any("not on a flat right" in n for n in sturt.notes)
    singh = ch.chamber(load_design(OLSEN / "singh-coal.yaml"))
    assert any("round wall" in n for n in singh.notes)
    tamba = ch.chamber(load_design(OLSEN / "tamba.yaml"))
    inlets = [p for p in tamba.patches if p.name.startswith("inlet flue")]
    assert len(inlets) == 4
    assert {p.face for p in inlets} == {"front 1"}
    r = rays.trace(list(tamba.zones), tamba.patches, rays=2_000, regions=tamba.regions(),
                   gas=[g.name for g in tamba.gas])  # fmt: skip
    assert r.lost == 0


def test_several_exit_flues_are_carved() -> None:
    exits = [
        {"through": "back", "count": 2, "port": {"width": "4.5 in", "height": "9 in"}},
        {"through": "floor", "count": 1, "port": {"width": "4.5 in", "height": "4.5 in"}},
    ]
    k = _design("fast-fire", {"draft.flue_port": None, "draft.exits": exits})
    patches, _ = ch.openings(k, DIMS)
    flues = [p for p in patches if p.name.startswith("exit flue")]
    assert [p.name for p in flues] == ["exit flue 1.1", "exit flue 1.2", "exit flue 2.1"]
    assert [p.face for p in flues] == ["back", "back", "floor"]
    assert flues[0].centre[0] == pytest.approx(-flues[1].centre[0])


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


BIG = 10.0
HALVES = (
    rays.Region(0, (-BIG, -BIG, -BIG), (0.0, BIG, BIG)),
    rays.Region(1, (0.0, -BIG, -BIG), (BIG, BIG, BIG)),
)
KS = (0.3, 3.0)


@pytest.fixture(scope="module")
def halves() -> rays.Rays:
    """The unit cube as two gas zones, its left and right halves."""
    return rays.trace(_cube_zones(), rays=50_000, regions=HALVES, gas=("a", "b"), ks=KS)


def test_two_gas_zones_obey_hottels_summation_rules(halves: rays.Rays) -> None:
    """A surface's row, Σ_j s_i s_j + Σ_z g_z s_i = A_i, exact after the closure; a gas zone's,
    Σ_i g_z s_i + Σ_w g_z g_w = 4kV_z, within the noise; each half's volume from its own chords
    (Cauchy per zone); the zones' g s sum to the one-zone trace's."""
    assert halves.gas_volumes == pytest.approx([0.5, 0.5], rel=5e-3)
    for k in (0.0, *KS):
        ss, gs, gg = halves.exchange_zones(k)
        assert np.abs(ss.sum(axis=1) + gs.sum(axis=0) - halves.areas).max() < 1e-12
        assert np.abs(ss - ss.T).max() < 1e-14
        assert np.abs(gg - gg.T).max() < 1e-14
        rows = gs.sum(axis=1) + gg.sum(axis=1)
        assert rows == pytest.approx(4 * k * halves.gas_volumes, rel=2e-3, abs=1e-12)
        _, one = halves.exchange(k)
        assert np.abs(gs.sum(axis=0) - one).max() < 1e-3
    _, gs0, gg0 = halves.exchange_zones(0.0)
    assert not gs0.any()
    assert not gg0.any()
    # The left wall sees the gas of its own half far more than the other's
    left = halves.index("left")
    _, gs, _ = halves.exchange_zones(3.0)
    assert gs[0, left] > 3 * gs[1, left]


def test_gas_zones_tile_the_rays_path() -> None:
    zones = _cube_zones()
    gap = (rays.Region(0, (-BIG, -BIG, -BIG), (-0.1, BIG, BIG)), HALVES[1])
    with pytest.raises(rays.GeometryError, match="isn't covered"):
        rays.trace(zones, rays=200, regions=gap, gas=("a", "b"))
    overlap = (rays.Region(0, (-BIG, -BIG, -BIG), (0.1, BIG, BIG)), HALVES[1])
    with pytest.raises(rays.GeometryError, match="isn't covered"):
        rays.trace(zones, rays=200, regions=overlap, gas=("a", "b"))
    with pytest.raises(rays.GeometryError, match="need their regions"):
        rays.trace(zones, rays=200, gas=("a",))
    with pytest.raises(rays.GeometryError, match="need their regions"):
        rays.trace(zones, rays=200, regions=HALVES, gas=("a",))


def test_an_untraced_absorption_coefficient_is_refused(halves: rays.Rays) -> None:
    with pytest.raises(rays.GeometryError, match="wasn't traced"):
        halves.exchange_zones(1.0)


def test_a_spheres_halves_absorb_its_closed_form() -> None:
    """A sphere's two halves as gas zones: their g s sum to the one-zone closed form, 1 − 2[1 −
    (1 + a)e^(−a)]/a² of the wall's emission, a = kD; each half half of it by symmetry."""
    s: Any = trimesh.creation.icosphere(subdivisions=4, radius=0.5)
    wall = rays.Zone("wall", np.asarray(s.triangles)[:, [0, 2, 1]])
    kd = 1.0
    r = rays.trace([wall], rays=50_000, regions=HALVES, gas=("a", "b"), ks=(kd,))
    _, gs, _ = r.exchange_zones(kd)
    eps = 1 - 2 * (1 - (1 + kd) * math.exp(-kd)) / kd**2
    assert gs.sum() / r.areas[0] == pytest.approx(eps, abs=5e-3)
    assert gs[0, 0] == pytest.approx(gs[1, 0], rel=2e-2)


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
