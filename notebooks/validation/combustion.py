"""Validation: combustion, available heat and Ward's burner-input ranges."""

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
    # Combustion and available heat (`kilndesigner.combustion`, `kilndesigner.gas`)

    - **Propane's flame temperature in air**: 3,595 °F (Propane Warehouse/Pro Tank Supply,
      `combustion-and-masonry.md` §1.1 [S1]). The engine's is Cantera's equilibrium adiabatic
      flame temperature, stoichiometric, air at 25 °C. Tolerance 1 %.
    - **Propane's lower heating value**: available heat with the flue at 25 °C is the heat of
      combustion with the water left as vapour, the LHV: GREET 46.607 MJ/kg [S5] and CARB
      46.66 MJ/kg [S5b]. Tolerance 1 %.
    - **Ward's burner input per ft³** (Ward Burner Systems Data Guide, §3.1 [S28]): the engine's
      table cell by cell, and Olsen's 10,000 BTU/ft³/hr for IFB (p.226) with his 20 ft³ worked
      example, 200,000 BTU/hr (p.227–228, `olsen-kilns.md` W16). Exact.

    **Not sourced, so not checked:** available heat at kiln flue temperatures. No published
    available-heat chart (the North American *Combustion Handbook*'s, for instance) is in
    `docs/research/`, so the fraction kept at 1000–1300 °C rests on Cantera's thermodynamics alone.
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.combustion import adiabatic_flame_temperature, available_heat
    from kilndesigner.gas import gas_data

    aft_f = adiabatic_flame_temperature() * 9 / 5 - 459.67
    lhv = available_heat(298.15) / 1e6
    results = [
        compare("propane flame temperature, °F", "§1.1 [S1]", aft_f, 3595, 0.01),
        compare("propane LHV, MJ/kg", "GREET, §1.1 [S5]", lhv, 46.607, 0.01),
        compare("propane LHV, MJ/kg", "CARB, §1.1 [S5b]", lhv, 46.66, 0.01),
    ]

    ward = {
        "hard_brick": [[12000, 17000], [14000, 18500], [16000, 20000]],
        "insulating_brick": [[6000, 10000], [8000, 13000], [10000, 16000]],
        "ceramic_fibre": [[4000, 6000], [6000, 8000], [7000, 10000]],
    }
    table = gas_data()["ward_btu_per_ft3_hr"]
    for wall, cells in ward.items():
        for cone, (low, high), engine in zip(table["columns"], cells, table["walls"][wall],
                                             strict=True):  # fmt: skip
            results.append(
                compare(f"Ward, {wall}, cone {cone}, low", "Ward [S28]", engine[0], low, 0)
            )
            results.append(
                compare(f"Ward, {wall}, cone {cone}, high", "Ward [S28]", engine[1], high, 0)
            )
    olsen_ifb = gas_data()["olsen_btu_per_ft3_hr"]["insulating_brick"][1]
    results.append(
        compare("Olsen W16: 20 ft³ IFB, BTU/hr", "Olsen p.227–228", 20 * olsen_ifb, 200_000, 0)
    )
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
