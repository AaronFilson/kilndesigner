"""Validation: sprung-arch geometry, brick counts and thrust against HarbisonWalker and Pitelka."""

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from published import compare, markdown

    return compare, markdown, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Arch thrust (`kilndesigner.frame`, `kilndesigner.shape`, `kilndesigner.masonry`)

    All from `docs/research/kiln-hardware.md` §4.3:

    - **HarbisonWalker's cold thrust** H/W for a circular arch, by rise per foot of span
      (1 to 3 in/ft) [S20]. HW prints two figures; tolerance 1 %.
    - **HarbisonWalker's heated arch** "free to rise", the hot thrust as a multiple of the cold, all
      73 printed cells (T/S 4–10 %), against the engine's statics with the thrust line at the arch
      faces (Heyman's maximum thrust). Tolerance 4.5 %: the worst cell is HW's "5.0" at T/S 7 %
      and 1 in/ft, printed to two figures beside "stress excessive", where the engine gives 5.20
      (+4.0 %); every other cell is within 3 %.
    - **HarbisonWalker's 12 ft worked example**: span 12 ft, 13½ in thick, 192 lb/ft³ basic
      brick, 2¼ in/ft. W = 3,032.64 lb/ft, H = 1,940.89 lb/ft, T/S taken as 9 %, so
      H_max = 1.84 H = 3,571.24 lb/ft. HW's W uses its rounded constant 1.17 DST; the engine weighs
      the ring along its mean arc (about 1 % less), and takes T/S as 9.375 %, not 9 %. Tolerances:
      W 1.5 %, H 2 %, H_max 3 %.
    - **Pitelka's two studio arches** at 2.3 in/ft [S4] [S11]: 45 in span, rise 8⅝ in, radius
      2 ft 9⅝ in, 18 No. 1 arches and 5 straights a ring; 36 in span, rise 6 15/16 in, radius
      2 ft 2 15/16 in, 18 No. 1 arches and one straight "in theory". Tolerance 1/16 in on the
      geometry; the counts exactly (the engine's 2½ in series brick, which Pitelka's counts fit).

    **Not checked:** HarbisonWalker's "Arch Combinations" brick counts (pp.71–72) are for 3 in
    series brick; the engine lays 2½ in series, so its counts can't be compared with them.
    """)
    return


@app.cell
def _(compare):
    import math

    from kilndesigner.frame import cold_thrust_factor, heated_thrust_factor
    from kilndesigner.geometry import ArchShape, Part
    from kilndesigner.masonry import IN, arch_ring
    from kilndesigner.shape import Arch

    hw = "HarbisonWalker [S20]"
    rises = (1, 1.25, 1.5, 1.608, 1.75, 2, 2.25, 2.302, 2.5, 2.75, 3)
    cold = (1.49, 1.18, 0.98, 0.91, 0.83, 0.72, 0.64, 0.62, 0.57, 0.51, 0.46)
    results = []
    for d, h_over_w in zip(rises, cold, strict=True):
        results.append(
            compare(f"cold H/W, {d} in/ft", hw, cold_thrust_factor(12.0, d), h_over_w, 0.01)
        )
    heated = {
        4: (1.88, 1.61, 1.47, 1.43, 1.39, 1.33, 1.29, 1.28, 1.26, 1.24, 1.22),
        5: (2.41, 1.86, 1.63, 1.59, 1.52, 1.43, 1.38, 1.37, 1.33, 1.29, 1.26),
        6: (3.29, 2.29, 1.94, 1.79, 1.67, 1.56, 1.47, 1.46, 1.42, 1.37, 1.33),
        7: (5.0, 2.80, 2.14, 1.98, 1.93, 1.69, 1.58, 1.57, 1.51, 1.45, 1.41),
        8: (None, 3.73, 2.55, 2.31, 2.17, 1.86, 1.70, 1.69, 1.60, 1.53, 1.48),
        9: (None, 5.34, 3.06, 2.75, 2.41, 2.04, 1.84, 1.81, 1.72, 1.63, 1.57),
        10: (None, None, 3.88, 3.30, 2.77, 2.22, 2.00, 1.95, 1.82, 1.73, 1.63),
    }
    for pct, row in heated.items():
        for d, factor in zip(rises, row, strict=True):
            if factor is None:  # "stress excessive"
                continue
            engine = heated_thrust_factor(12.0, d, 12.0 * pct / 100)
            assert engine is not None
            results.append(compare(f"hot/cold, T/S {pct} %, {d} in/ft", hw, engine, factor, 0.045))

    # HarbisonWalker's 12 ft example, in inches and lb/ft
    span, thick, density = 144.0, 13.5, 192.0
    arch = Arch(span, 2.25 * span / 12)
    weight = density * (thick / 12) * (arch.radius + thick / 2) * 2 * arch.half_angle / 12
    h_cold = cold_thrust_factor(span, arch.rise) * weight
    hot = heated_thrust_factor(span, arch.rise, thick)
    assert hot is not None
    results += [
        compare("HW 12 ft: W, lb/ft", hw, weight, 3032.64, 0.015),
        compare("HW 12 ft: H, lb/ft", hw, h_cold, 1940.89, 0.02),
        compare("HW 12 ft: H_max, lb/ft", hw, hot * h_cold, 3571.24, 0.03),
    ]

    # Pitelka's arches: geometry and the ring of 4½ in deep arch brick
    pitelka = "Pitelka [S4] [S11]"
    for span_in, rise_in, radius_in, shaped, straights in (
        (45, 8.625, 33.625, 18, 5),
        (36, 6 + 15 / 16, 26 + 15 / 16, 18, 1),
    ):
        a = Arch(span_in, 2.3 * span_in / 12)
        results += [
            compare(f"Pitelka {span_in} in: rise, in", pitelka, a.rise, rise_in, 1 / 16,
                    absolute=True),
            compare(f"Pitelka {span_in} in: radius, in", pitelka, a.radius, radius_in, 1 / 16,
                    absolute=True),
        ]  # fmt: skip
        mm = Arch(span_in * IN, a.rise * IN)
        part = Part(
            "roof/1-ifb",
            "ifb-jm26",
            "insulating_firebrick",
            (0.0, 0.0, 0.0),
            (span_in * IN, 9 * IN, a.rise * IN),
            arch=ArchShape(mm.radius, 4.5 * IN, 0.0, mm.half_angle),
            face="roof",
        )
        ring = arch_ring(part)
        assert ring is not None
        assert ring.shape == "No. 1 arch"
        results += [
            compare(f"Pitelka {span_in} in: No. 1 arches", pitelka, ring.shaped, shaped, 0,
                    absolute=True),
            compare(f"Pitelka {span_in} in: straights", pitelka, ring.straights, straights, 0,
                    absolute=True),
        ]  # fmt: skip
    assert math.isclose(Arch(12.0, 1.608).half_angle, math.pi / 6, rel_tol=1e-3)
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
