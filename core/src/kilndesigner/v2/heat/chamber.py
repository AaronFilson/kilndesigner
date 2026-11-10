"""The chamber the heat model radiates in, from the engine's own solids and layout: the gas volume
as `massing._cavity` draws it (the solid the 3-D model and the statics are cut from), its faces
named by where they are, and the design's openings carved from them: the exit flue, under-floor
inlet flues (the engine's layout, `firebox_parts.openings`), spy holes and burner ports.

Frame (geometry.py's): metres here, x across, y from the firing end to the flue end, z up from the
chamber's floor; the chamber centred on x = y = 0. A wall's "across" is to your right standing
outside and facing it, as the design file has it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from kilndesigner.model import Kiln
from kilndesigner.units import si
from kilndesigner.v2.heat.rays import Patch, Zone, solid_zones

MM = 1e-3
COURSE = 2.5 * 0.0254  # a 2½ in course: the engine lays burner ports one course up

WALLS = ("left", "right", "front", "back")


class NotModelledError(ValueError):
    """A chamber or opening the heat model doesn't take yet."""


@dataclass(frozen=True)
class Chamber:
    """The chamber's inside: its zones, its openings, its size (m) and gas volume (m³)."""

    zones: tuple[Zone, ...]
    patches: tuple[Patch, ...]
    width: float
    depth: float
    height: float
    volume: float
    notes: tuple[str, ...] = ()


def _classify(w: float, d: float) -> Any:
    """Name a face of the cavity (mm) by where it is: the floor at z = 0, the four walls by their
    planes (the end walls' segments over the springline with their walls), the rest the roof."""

    def name(face: Any) -> str:
        c = face.center()
        if abs(c.Z) < 1e-3:
            return "floor"
        if face.geom_type.name == "PLANE":
            n = face.normal_at(c)
            if abs(n.Y) > 0.999 and abs(abs(c.Y) - d / 2) < 1e-3:
                return "front" if c.Y < 0 else "back"
            if abs(n.X) > 0.999 and abs(abs(c.X) - w / 2) < 1e-3:
                return "left" if c.X < 0 else "right"
        return "roof"

    return name


def cavity(kiln: Kiln) -> tuple[list[Zone], float, tuple[float, float, float]]:
    """The gas volume's zones, its volume (m³) and (width, depth, springline), from the engine's
    own solid. One straight box chamber only for now; the rest are refused with the reason."""
    from kilndesigner.massing import (
        _cavity,  # pyright: ignore[reportPrivateUsage]
        cells,
        run_of,
    )

    run = run_of(kiln)
    if run.round or run.chambers > 1 or run.bend > 0 or run.slope > 0 or run.widths:
        raise NotModelledError(
            "one straight box chamber is modelled so far; round chambers, rows, bends, slopes "
            "and changing widths wait for zones in series"
        )
    (cell,) = [c for c in cells(kiln, run) if c.kind == "box"]
    solid = _cavity(kiln, run, cell, 0.0)
    zones = solid_zones(solid, _classify(run.width, cell.length))
    return zones, float(solid.volume) * MM**3, (run.width * MM, run.depth * MM, run.height * MM)


def wall_patch(
    name: str, wall: str, size: tuple[float, float], across: float, up: float, dims: Any
) -> Patch:
    """A rectangle (width, height, m) on a wall, its centre ``across`` to the right seen from
    outside and ``up`` from the floor; u × v points into the gas."""
    w, h = size
    width, depth, _ = dims
    if wall == "front":
        return Patch(name, wall, (across, -depth / 2, up), (0, 0, 1), (1, 0, 0), (h / 2, w / 2))
    if wall == "back":
        return Patch(name, wall, (-across, depth / 2, up), (1, 0, 0), (0, 0, 1), (w / 2, h / 2))
    if wall == "left":
        return Patch(name, wall, (-width / 2, -across, up), (0, 1, 0), (0, 0, 1), (w / 2, h / 2))
    if wall == "right":
        return Patch(name, wall, (width / 2, across, up), (0, 0, 1), (0, 1, 0), (h / 2, w / 2))
    raise NotModelledError(f"an opening in the {wall} isn't placed yet")


def _size(port: Any) -> tuple[float, float, bool]:
    w, h = port.size_in()
    if port.round:  # a round hole as the square of its area (said in the working)
        side = math.sqrt(math.pi / 4) * w
        return side * 0.0254, side * 0.0254, True
    return w * 0.0254, h * 0.0254, False


def openings(kiln: Kiln, dims: tuple[float, float, float]) -> tuple[list[Patch], list[str]]:
    """The design's openings as patches, and what was said about them."""
    out: list[Patch] = []
    notes: list[str] = []
    draft = kiln.draft
    if draft is not None and draft.flue_port is not None and draft.type != "up":
        w, h, rnd = _size(draft.flue_port)
        across = si(draft.flue_across, "m") if draft.flue_across is not None else 0.0
        out.append(wall_patch("exit flue", draft.flue_wall, (w, h), across, h / 2, dims))
        if rnd:
            notes.append("the round exit flue taken as the square of its area")
    elif draft is not None and draft.exits is not None:
        raise NotModelledError("several exit flues (draft.exits) aren't carved yet")
    fire = kiln.heat.fire
    if fire is not None:
        from kilndesigner.firebox_parts import openings as fire_openings

        for k, o in enumerate(o for o in fire_openings(kiln) if o.name.endswith("/inlet")):
            (x0, y0, _), (x1, y1, _) = o.lo, o.hi
            half = ((x1 - x0) / 2 * MM, (y1 - y0) / 2 * MM)
            cx, cy = (x0 + x1) / 2 * MM, (y0 + y1) / 2 * MM
            # On the floor whole, its printed size kept
            mx = min(max(cx, -dims[0] / 2 + half[0]), dims[0] / 2 - half[0])
            my = min(max(cy, -dims[1] / 2 + half[1]), dims[1] / 2 - half[1])
            if max(abs(mx - cx), abs(my - cy)) > 1e-6:
                notes.append(
                    f"inlet flue {k + 1}: the engine's layout puts it {abs(mx - cx) * 1e3:.0f} × "
                    f"{abs(my - cy) * 1e3:.0f} mm off the floor (under a wall); moved onto the "
                    "floor at its size"
                )
            centre = (mx, my, 0.0)
            out.append(Patch(f"inlet flue {k + 1}", "floor", centre, (1, 0, 0), (0, 1, 0), half))
    gas = kiln.heat.gas
    if gas is not None and gas.burners.count is not None and gas.burners.wall != "floor":
        from kilndesigner.firebox_parts import burner_port_in

        size = burner_port_in(kiln)
        if size is None:
            notes.append("the burner ports' size isn't given: their openings are left out")
        else:
            pw, ph = size[0] * 0.0254, size[1] * 0.0254
            if size[2]:
                pw = ph = math.sqrt(math.pi / 4) * pw
            up = si(gas.burners.up, "m") if gas.burners.up is not None else COURSE + ph / 2
            wall = gas.burners.wall
            length = dims[1] if wall in ("left", "right") else dims[0]
            n = gas.burners.count
            for i in range(n):
                across = length * ((i + 0.5) / n - 0.5)
                out.append(wall_patch(f"burner port {i + 1}", wall, (pw, ph), across, up, dims))
            notes.append("burner ports spread evenly along their wall, as the engine lays them")
    spies = kiln.spy_holes.holes if kiln.spy_holes is not None else None
    for i, hole in enumerate(spies or []):
        if hole.wall == "roof":
            notes.append(f"spy hole {i + 1} is in the roof: not carved yet, left out")
            continue
        w, h, _ = _size(hole.port)
        up = si(hole.up, "m") if hole.up is not None else h / 2
        across = si(hole.across, "m")
        out.append(wall_patch(f"spy hole {i + 1}", hole.wall, (w, h), across, up, dims))
    return out, notes


def chamber(kiln: Kiln) -> Chamber:
    zones, volume, dims = cavity(kiln)
    patches, notes = openings(kiln, dims)
    return Chamber(tuple(zones), tuple(patches), *dims, volume, tuple(notes))
