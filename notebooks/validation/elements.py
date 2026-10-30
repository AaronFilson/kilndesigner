"""Validation: electric element design against Kanthal's, Olsen's and Krueger's numbers."""

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
    # Element design (`kilndesigner.electric`, `kilndesigner.library`)

    - **Kanthal's worked example** (`electric-and-thermal.md` §1.7 [S16]): 20 kW at 220 V,
      Kanthal AF at 1200 °C, 4.0 W/cm². Kanthal: d ≈ 4.98 mm; with the standard 5.0 mm wire,
      3.95 W/cm². The 32.25 m length is derived in the notes from Kanthal's inputs. Tolerance: the
      last printed figure.
    - **Olsen's 26 kW element** (*The Kiln Book*, 4th ed., p.258–260; `olsen-kilns.md` W25): six
      groups of 4333 W at 240 V, 8 W/in², Ct 1.04; B&S 10 wire; 154.2 ft a group at 7.4 W/in².
      Olsen takes 0.083 Ω/ft for B&S 10; the engine uses Kanthal A-1's 1.45 Ω·mm²/m and ASTM B258's
      diameter, 0.0840 Ω/ft, so its length is about 1 % shorter. Tolerance 2 % on length, 0.5 %
      on load; the wire chosen for 8 W/in² must round to B&S 10.
    - **Ct tables** for A-1, APM, AF, D and Nikrothal 80 from the Kanthal data sheets
      (§1.2 [S1–S5]): every printed row, to the table's two decimals (±0.005).
    - **AWG (B&S) diameters**, ASTM B258 as tabled in §2 [S19]: ±0.001 mm.
    - **Krueger's 240 V, 24 A replacement element** (§1.6 [S15]): coil OD 0.4570 in, A-1 at
      about 17.5 W/in² in a kiln rated about 2300 °F. Krueger gives no gauge, so what can be
      checked is the coil: the engine's wire for 5760 W at 240 V and 17.5 W/in², coiled at
      Kanthal's 5 d for grooves, against Krueger's 0.457 in. Tolerance 2 %.

    **Recorded, not checked:** Skutt's three-phase nameplates (`electrical-supply.md` §4 [E5]).
    KM1027 3-ph 240 V, 11,520 W, lists 29.3 A; P/(√3·V) gives 27.7 A (−5.5 %). KM1227-3 PK 240 V,
    14,300 W, lists 40.0 A; P/(√3·V) gives 34.4 A (−14 %). The research notes that makers' figures
    include controls and rounding and that the nameplate, not the derived current, sizes the
    breaker; the engine works from the breaker the user gives, so these nameplates can't be
    reproduced and no published three-phase element design was found.
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.electric import surface_load, wire_diameter, wire_length
    from kilndesigner.library import alloy, awg_diameter
    from kilndesigner.units import Q_, si

    results = []

    # Kanthal's example
    af = alloy("kanthal-af")
    kanthal = "Kanthal [S16], §1.7"
    ct = af.temperature_factor(Q_(1200, "degC"))
    rho_t = si(af.resistivity, "ohm*m") * ct
    d = wire_diameter(20_000, 220, 4.0e4, rho_t)
    length = wire_length(20_000, 220, 5.0e-3, rho_t)
    results += [
        compare("Kanthal: d, mm", kanthal, d * 1000, 4.98, 0.005, absolute=True),
        compare("Kanthal: L, m (derived)", kanthal, length, 32.25, 0.005, absolute=True),
        compare(
            "Kanthal: load on 5.0 mm, W/cm²",
            kanthal,
            surface_load(20_000, 5.0e-3, length) / 1e4,
            3.95,
            0.005,
            absolute=True,
        ),
    ]

    # Olsen's 26 kW kiln, with the engine's own A-1 data and AWG 10
    a1 = alloy("kanthal-a1")
    olsen = "Olsen p.258–260"
    group, volts = 26_000 / 6, 240
    rho_hot = si(a1.resistivity, "ohm*m") * 1.04
    chosen = wire_diameter(group, volts, si(Q_(8, "W/in**2"), "W/m**2"), rho_hot)
    gauge = min(range(8, 21), key=lambda g: abs(si(awg_diameter(g), "m") - chosen))
    results.append(compare("Olsen: B&S gauge for 8 W/in²", olsen, gauge, 10, 0, absolute=True))
    d10 = si(awg_diameter(10), "m")
    olsen_length = wire_length(group, volts, d10, rho_hot)
    results += [
        compare("Olsen: length a group, ft", olsen, olsen_length / 0.3048, 154.2, 0.02),
        compare(
            "Olsen: actual load, W/in²",
            olsen,
            surface_load(group, d10, olsen_length) * 0.0254**2,
            7.4,
            0.005,
        ),
    ]

    # Ct, every printed row (Kanthal data sheets)
    rows = (100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400)
    ct_tables = {
        "kanthal-a1": (1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04,
                       1.04, 1.05),
        "kanthal-apm": (1.00, 1.00, 1.00, 1.00, 1.01, 1.02, 1.02, 1.03, 1.03, 1.04, 1.04, 1.04,
                        1.04, 1.05),
        "kanthal-af": (1.00, 1.01, 1.01, 1.02, 1.03, 1.04, 1.04, 1.05, 1.05, 1.06, 1.06, 1.06,
                       1.06),
        "kanthal-d": (1.00, 1.01, 1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07, 1.07, 1.07, 1.08,
                      1.08),
        "nikrothal-80": (1.01, 1.02, 1.03, 1.04, 1.05, 1.04, 1.04, 1.04, 1.04, 1.05, 1.06,
                         1.07),
    }  # fmt: skip
    for alloy_id, values in ct_tables.items():
        alloy_data = alloy(alloy_id)
        for t, value in zip(rows, values, strict=False):
            results.append(
                compare(
                    f"Ct, {alloy_data.name}, {t} °C",
                    "Kanthal data sheet, §1.2",
                    alloy_data.temperature_factor(Q_(t, "degC")),
                    value,
                    0.005,
                    absolute=True,
                )
            )

    # AWG
    for g, mm in ((8, 3.264), (10, 2.588), (11, 2.305), (12, 2.053), (14, 1.628), (20, 0.812)):
        results.append(
            compare(f"AWG {g}, mm", "B258 table, §2 [S19]", si(awg_diameter(g), "mm"), mm, 0.001,
                    absolute=True)
        )  # fmt: skip

    # Krueger's 240 V 24 A element
    krueger = "Krueger [S15], §1.6"
    rho_k = si(a1.resistivity, "ohm*m") * a1.temperature_factor(Q_(2300, "degF"))
    d_k = wire_diameter(240 * 24, 240, si(Q_(17.5, "W/in**2"), "W/m**2"), rho_k)
    results.append(compare("Krueger: coil OD at 5 d, in", krueger, 5 * d_k / 0.0254, 0.457, 0.02))
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
