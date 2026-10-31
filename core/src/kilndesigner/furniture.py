"""Kiln furniture and the setting's weight: the shelves and posts a design describes, weighed from
sourced densities, and the ware as a multiple of them.

Olsen weighs 12 × 24 × 1 in shelves (The Kiln Book, 4th ed., p.33–35; kiln-reference.md, "Kiln
furniture"): mullite about 20.5 lb, conventional silicon carbide about 22 lb, cordierite up to
21 lb. Each density here is that weight over the shelf's 288 in³. A post of the same material is
weighed at the same density. Advancer (nitride-bonded SiC, 8 lb) is left out: its thickness is not
legible in the scan (p.35, "5/16 in (?)"), so its density can't be worked out. No source here
gives a post's size, so a design's posts are the user's.

The ware's weight is a ratio of the setting's, set by the design from 0 (an empty setting) up;
the author's typical load is 6 to 8 times the setting (the user, 2026-10-30), not a published
source, so 7, the middle, by default.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from kilndesigner.units import Q_, si
from kilndesigner.working import Step

if TYPE_CHECKING:
    from kilndesigner.model import Setting

OLSEN_SHELVES = "Olsen, The Kiln Book, 4th ed., p.33–35 (kiln-reference.md, Kiln furniture)"
SHELF_IN3 = 12 * 24 * 1  # the shelf Olsen weighs, in³
SHELF_WEIGHT_LB: dict[str, float] = {
    "mullite": 20.5,
    "silicon-carbide": 22.0,
    "cordierite": 21.0,  # "up to": the most, so the setting isn't under-weighed
}
"""Olsen's 12 × 24 × 1 in shelf, by material (lb)."""

WARE_RATIO_TYPICAL = (6.0, 8.0)  # the author's typical load, not a limit
WARE_RATIO_DEFAULT = 7.0
WARE_RATIO_SOURCE = (
    "the author (the user, 2026-10-30): ware typically weighs about 6 to 8 times the setting; "
    "the design sets its own; not a published source"
)


def density_lb_in3(material: str) -> float:
    """A furniture material's density (lb/in³), from Olsen's shelf weights."""
    if material not in SHELF_WEIGHT_LB:
        raise ValueError(
            f"no sourced density for kiln furniture of '{material}': Olsen weighs shelves of "
            f"{', '.join(SHELF_WEIGHT_LB)} (p.33–35); no other is weighed in a source here"
        )
    return SHELF_WEIGHT_LB[material] / SHELF_IN3


def setting_weight(setting: Setting) -> tuple[float, float, list[Step]]:
    """The setting's weight and the ware's (kg), with the working."""
    sh = setting.shelves
    ln, w, t = si(sh.length, "in"), si(sh.width, "in"), si(sh.thickness, "in")
    shelf = ln * w * t * density_lb_in3(sh.material)
    shelves = shelf * sh.per_layer * sh.layers
    steps = [
        Step(
            name="Shelves",
            value=f"{shelves:.0f} lb",
            formula="L × W × T × ρ × per layer × layers, ρ = Olsen's shelf weight ÷ 288 in³",
            inputs={
                "size": f"{ln:g} × {w:g} × {t:g} in",
                "ρ": f"{sh.material}, {SHELF_WEIGHT_LB[sh.material]:g} lb per 12 × 24 × 1 in",
                "each": f"{shelf:.1f} lb",
                "count": f"{sh.per_layer} a layer × {sh.layers} layers",
            },
            reference=OLSEN_SHELVES,
        )
    ]
    posts = 0.0
    if setting.posts is not None:
        p = setting.posts
        pw, pd, ph = si(p.width, "in"), si(p.depth, "in"), si(p.height, "in")
        post = pw * pd * ph * density_lb_in3(p.material)
        posts = post * p.per_layer * sh.layers
        steps.append(
            Step(
                name="Posts",
                value=f"{posts:.0f} lb",
                formula="W × D × H × ρ × per layer × layers",
                inputs={
                    "size": f"{pw:g} × {pd:g} in, {ph:g} in high",
                    "ρ": f"{p.material}, as Olsen's shelves of it",
                    "each": f"{post:.2f} lb",
                    "count": f"{p.per_layer} a layer × {sh.layers} layers",
                },
                reference=f"{OLSEN_SHELVES}; the posts' size is the design's",
            )
        )
    furniture = shelves + posts
    ratio = setting.ware_ratio
    ware = ratio * furniture
    steps += [
        Step(
            name="Setting",
            value=f"{furniture:.0f} lb",
            formula="shelves + posts",
            note=None if setting.posts is not None else "No posts given: shelves only.",
        ),
        Step(
            name="Ware",
            value=f"{ware:.0f} lb",
            formula="ratio × setting",
            inputs={"ratio": f"{ratio:g}"},
            reference=WARE_RATIO_SOURCE,
        ),
        Step(name="Setting and ware", value=f"{furniture + ware:.0f} lb", formula="setting + ware"),
    ]
    return si(Q_(furniture, "lb"), "kg"), si(Q_(ware, "lb"), "kg"), steps
