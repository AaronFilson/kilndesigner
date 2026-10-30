"""Validation: propane cylinders, tanks and regulator pressure against published figures."""

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
    # Propane supply (`kilndesigner.gas`, `kilndesigner.gas_checks`)

    All from `combustion-and-masonry.md` §1.2 and §2:

    - **Tanks, D × L × K** (§2.3 [S1, S12]): capacity at 0 °F = outside diameter × length × K.
      The source's 1,000 gal tank is 41 × 192 in; the ⅓-full table's 120 gal row is 24 × 60 in
      (§2.8). At ⅓ full K is 73.3, between the published 30 % (70) and 40 % (80) rows. The
      engine's ⅓-full capacity at 0 °F must equal D × L × 73.3. Tolerance 0.5 %.
    - **Tank ceilings, Ward** (§2.4 [S23]): a 500 gal tank **60 %** full gives about
      425,000 BTU/hr at 0 °F and 850,000 at 20 °F. The engine's tank is only ⅓ full, so it must
      come in under Ward's figures (a ceiling, not a match).
    - **Cylinder ceilings** (§2.1 [S3], §2.2 [S10, S11]): a full 100 lb cylinder, read at the
      liquid's temperature, 20 °F under 60 °F air: the 40 °F column, 214,000 BTU/hr; the
      conservative case (vertical, ¼ full, at least 10 psi) at 60 °F: 79,700. Exact.
    - **Vapour pressure**: Ward's "about 77 psi at 50 °F, about 23 psi at 0 °F" (§1.2 [S23]),
      an independent check on the NIST table the engine reads. Tolerance 5 % ("about").
    - **The regulator**: RegO's 597FB, set at 20 psig, delivers about 16 psig at full flow on a
      50 psig inlet (§2.8 [S89]); the engine's most the burners are sure of, from 50 psig in the
      container. Exact.

    **Not sourced, so not checked:** the D × L × K example's −10 °F case (236,160 BTU/hr): the
    engine's tables stop at 0 °F and it doesn't extrapolate below (ADR 0009).
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.gas import _supply_cases, gas_data, interpolate
    from kilndesigner.gas_checks import pressure_ceiling
    from kilndesigner.model import Cylinders, Gas, Tank

    def capacity(supply, t_f, which=0):
        gas = Gas.model_validate({"supply": supply.model_dump()})
        cases, _ = _supply_cases(gas, 0.0, t_f)
        return cases[which].capacity_btu_hr

    k_third = 70 + (100 / 3 - 30) * (80 - 70) / 10
    dlk = "D × L × K, §2.3 [S12]"
    ward = "Ward, 500 gal 60 % full [S23]"
    vapour = gas_data()["vapour_pressure"]
    one = Cylinders(count=1)
    results = [
        compare("1000 gal, ⅓ full, 0 °F", dlk, capacity(Tank(gallons=1000), 0), 41 * 192 * k_third,
                0.005),
        compare("120 gal, ⅓ full, 0 °F", dlk, capacity(Tank(gallons=120), 0), 24 * 60 * k_third,
                0.005),
        compare("500 gal, 0 °F, under Ward", ward, capacity(Tank(gallons=500), 0), 425_000, 0,
                ceiling=True),
        compare("500 gal, 20 °F, under Ward", ward, capacity(Tank(gallons=500), 20), 850_000, 0,
                ceiling=True),
        compare("100 lb full, 60 °F air", "Flame Engineering [S3]", capacity(one, 60), 214_000,
                0),
        compare("100 lb ¼ full, 10 psi, 60 °F", "§2.2 [S10]", capacity(one, 60, 2),
                79_700, 0),
        compare("vapour pressure 50 °F, psig", "Ward [S23]",
                interpolate(50, vapour["temps_f"], vapour["psig"]), 77, 0.05),
        compare("vapour pressure 0 °F, psig", "Ward [S23]",
                interpolate(0, vapour["temps_f"], vapour["psig"]), 23, 0.05),
        compare("597FB on 50 psig, psig", "RegO 597F [S89]", pressure_ceiling(50.0), 16.0, 0),
    ]  # fmt: skip
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
