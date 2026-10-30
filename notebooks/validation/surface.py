"""Validation: surface convection and radiation against published data (ADR 0009)."""

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
    # Surface convection and radiation (`kilndesigner.thermal.surface`, `thermal.air`)

    What is published, and checked here:

    - **Air at 300 K**: ν = 1.572 × 10⁻⁵ m²/s and Pr = 0.712, from Neutrium's table (Holman's
      Table A-5 values), cross-checked against Çengel Table A-9 (`electric-and-thermal.md` §6.3
      [S63, S84]). Tolerance 0.1 %.
    - **The correlations' constants**, against `ht` (Caleb Bell's open implementation of the
      textbook correlations), an independent code: Churchill–Chu for a vertical plate; McAdams
      (Lloyd–Moran constants) for a hot face up, 0.54 Ra^¼ / 0.15 Ra^⅓; and for a **hot face down**,
      0.27 Ra^¼ (§6.2 [S62]; three sources in `thermal-properties.md` §5 [T30, T32]). Tolerance
      1 % (McAdams's laminar–turbulent switch sits at a slightly different Ra in `ht`).
    - **Radiation**: h_r = εσ(T_s² + T∞²)(T_s + T∞) (§6.2), against `ht.radiation.q_rad`, the net
      grey-body flux, divided by the temperature difference. Tolerance 10⁻⁵ (`ht` takes σ to
      more figures than the engine's 5.670374 × 10⁻⁸).

    **Not sourced, so not checked:** a published worked example with numbers for the radiation
    coefficient, or for a hot face down (the research files hold the formulas and the constants,
    not a solved case). FOSSEE's Example 6.11 splits its films into convection and radiation
    (16.5 + 17.5 and 12.5 + 6.5 W/m²K) but gives no emissivity or surface temperature to
    reproduce them. These rows check the engine against an independent implementation, not a
    published number.
    """)
    return


@app.cell
def _(compare):
    from ht.conv_free_immersed import (  # pyright: ignore[reportMissingTypeStubs]
        Nu_horizontal_plate_McAdams,
        Nu_vertical_plate_Churchill,
    )
    from ht.radiation import q_rad  # pyright: ignore[reportMissingTypeStubs]

    from kilndesigner.thermal.air import air
    from kilndesigner.thermal.surface import nusselt, radiation_coefficient

    a300 = air(300.0)
    neutrium = "Neutrium/Holman, §6.3 [S63]"
    results = [
        compare("ν at 300 K, m²/s", neutrium, a300.kinematic_viscosity, 1.572e-5, 1e-3),
        compare("Pr at 300 K", neutrium, a300.prandtl, 0.712, 1e-3),
    ]
    pr = 0.71
    for ra in (1e3, 1e6, 1e9):
        results.append(
            compare(
                f"vertical, Ra {ra:.0e}",
                "Churchill–Chu, `ht`",
                nusselt("vertical", ra, pr),
                Nu_vertical_plate_Churchill(pr, ra / pr),
                1e-6,
            )
        )
    for ra in (1e5, 1e6, 1e8, 1e10):
        results.append(
            compare(
                f"hot face up, Ra {ra:.0e}",
                "McAdams, `ht`",
                nusselt("facing_up", ra, pr),
                Nu_horizontal_plate_McAdams(pr, ra / pr, buoyancy=True),
                1e-2,
            )
        )
        results.append(
            compare(
                f"hot face down, Ra {ra:.0e}",
                "McAdams 0.27 Ra^¼, `ht`",
                nusselt("facing_down", ra, pr),
                Nu_horizontal_plate_McAdams(pr, ra / pr, buoyancy=False),
                1e-2,
            )
        )
    for eps, ts, ta in ((0.79, 350.0, 300.0), (0.9, 450.0, 294.0), (1.0, 400.0, 300.0)):
        results.append(
            compare(
                f"h_r, ε {eps}, {ts:.0f} K into {ta:.0f} K",
                "grey body, `ht.q_rad`",
                radiation_coefficient(eps, ts, ta),
                q_rad(eps, ts, ta) / (ts - ta),
                1e-5,
            )
        )
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
