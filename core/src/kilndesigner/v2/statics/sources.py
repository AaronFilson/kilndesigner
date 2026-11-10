"""The sourced values v2's statics uses, each with its reference in `docs/research/`.

Nothing here is fitted to a reference kiln (ADR 0017, decision 4). A value with no source is
carried as a band, or as a stand-in the user decided, and the working says so.
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.library import Material, material
from kilndesigner.units import Q_, parse_quantity, si


@dataclass(frozen=True)
class Sourced:
    """A value (SI) with where it comes from, and a note when it is a stand-in or flagged."""

    value: float
    reference: str
    note: str | None = None


PSI = si(Q_(1, "psi"), "Pa")

MU_COLD = Sourced(
    0.60,
    "BIA TN 31A: 'at least 0.60' between the units of a brick masonry arch (flat-roofs.md "
    "§2.2); Oliveira et al. 2021: 30.9° on dry refractory joints at 20 °C, μ 0.60 "
    "(mortar-and-brick-strength.md S1)",
)
MU_HOT = Sourced(
    0.50,
    "Oliveira et al. 2021: 26.5° at 300 °C, the lowest of their 300–900 °C tests, μ 0.50 "
    "(mortar-and-brick-strength.md S1)",
    "measured on dense alumina-spinel brick; IFB and fireclay weren't tested, so for them it is "
    "flagged, not claimed",
)
MU_SUPPORT_NOTE = (
    "brick on steel, earth or concrete: no friction coefficient is sourced (flat-roofs.md §2.4: "
    "'NOT FOUND'), so it is carried as a band from 0 (frictionless) to the masonry's own value"
)

C16_IFB = Sourced(
    10 * PSI,
    "ASTM C16 hot load for insulating firebrick, 10 psi held 1½ h: Morgan K-23 0 and 0.3 %, "
    "K-25 0 and 0.1 % at 2000 and 2200 °F (morgan-k-ifb-sheets.md §5; refractory-bearing.md)",
    "a stand-in for IFB's hot crushing strength, which no source gives (the user's decision, "
    "2026-11-10); real hot crushing and creep data are to be found",
)
C16_DENSE = Sourced(
    25 * PSI,
    "ASTM C16-03 §7.1, the load test for dense shapes: 'Apply a load of 25 psi (172 kPa)' "
    "(refractory-bearing.md B1.2)",
    "the user's IFB stand-in carried over to dense firebrick by analogy, a question for the user; "
    "dense fireclay subsides 1.3–6.8 % under it at 2460–2640 °F, so it is not a safe limit",
)

COURSE = Sourced(
    si(Q_(2.5, "inch"), "m"),
    "Olsen, The Kiln Book, 4th ed., pp.19–20: the 9 × 4½ × 2½ in brick, laid flat in 2½ in "
    "courses (kiln-reference.md)",
    "the design file gives no course height; the courses are evened to the springline",
)


IFB_GROWTH = Sourced(
    0.008,
    "IFB 0.5–0.7 % reversible to about 1000 °C (Morgan JM and TJM, H.S. Walsh class 26; "
    "thermal-properties.md §2.1), 0.7–0.8 % at most (Morgan K-23, K-25, K-26, 2025; "
    "morgan-k-ifb-sheets.md §7)",
    "the band 0.5–0.8 %, the ring taken at its hot face's temperature throughout (more growth than "
    "a ring cooler outside: the cautious end for the frame) until v2's heat model gives its mean",
)
IFB_GROWTH_LOW = 0.005
FIRECLAY_GROWTH = Sourced(
    3 / 32 / 12,
    "fireclay brick 3/32 in a foot from room temperature to 2400 °F, the makers' expansion "
    "allowance (Brosnan, refractory-movement-and-mortar.md §1.1.1 [M1]); half is enough, the "
    "joints taking the rest (Bhatia [M2])",
    "the band 3/64 to 3/32 in a foot; the cautious end for the frame is the whole",
)


def growth(material_id: str) -> tuple[float, float, Sourced] | None:
    """The reversible strain of a ring of this material at full temperature: (low, high, source),
    or None where no source gives one (castables, building brick, stone)."""
    kind = material(material_id).kind
    if kind == "insulating_firebrick":
        return IFB_GROWTH_LOW, IFB_GROWTH.value, IFB_GROWTH
    if kind == "dense_firebrick":
        return FIRECLAY_GROWTH.value / 2, FIRECLAY_GROWTH.value, FIRECLAY_GROWTH
    return None


def density(material_id: str) -> float:
    """kg/m³, from the materials library."""
    return si(parse_quantity(material(material_id).density), "kg/m**3")


def density_reference(material_id: str) -> str:
    m: Material = material(material_id)
    return f"materials.yaml {material_id}: {m.density} ({m.source})"


def crushing(material_id: str) -> Sourced | None:
    """The hot crushing stand-in for a material, by its kind: IFB the C16 10 psi the user
    decided; dense firebrick C16's 25 psi by analogy; any other: none (Heyman's unlimited
    compression)."""
    kind = material(material_id).kind
    if kind == "insulating_firebrick":
        return C16_IFB
    if kind == "dense_firebrick":
        return C16_DENSE
    return None


def by_analogy(material_id: str) -> bool:
    """Whether the material's crushing stand-in is carried over by analogy rather than decided
    (dense firebrick's 25 psi, a question for the user): a verdict that rests on it alone isn't
    given (ADR 0009), the missing data said instead."""
    return crushing(material_id) is C16_DENSE
