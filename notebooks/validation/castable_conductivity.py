"""Validation: the cast-mix conductivity law on Morgan castables it was not fitted to."""

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
    # Castable conductivity law (`kilndesigner.castable.conductivity_law`)

    The law k = a·(ρ/1000)ⁿ·(1 + s·(T − 400 °C)/1000) is fitted to nine insulating firebricks'
    published k(T). Here it predicts insulating castables it never saw, from Morgan's data sheets
    (`masonry-materials.md` §5.1–5.2), at each one's fired density (the low end where a range is
    given, as the engine's held-out set does):

    - **Firelite 2600LI** [M24], 1140 kg/m³ after 5 h at 815 °C: 0.38, 0.38, 0.38, 0.39, 0.39
      W/(m·K) at 200, 400, 600, 800 and 1000 °C.
    - **Kaolite 2600LI Pump** [M20], fired at 816 °C 1201–1442 kg/m³: 0.39, 0.42, 0.43, 0.46 at
      260, 538, 816 and 1093 °C.
    - **Kaolite 2600LI Gun** [M21], fired at 816 °C 1250–1410 kg/m³: 0.42, 0.42, 0.43, 0.46 at the
      same temperatures. This sheet is not in the engine's held-out set; it is a third check.

    Tolerance: 25 %, the leave-one-out error on the bricks that the engine quotes with every
    castable result. The engine also quotes the held-out band, about −9 % to +22 %.
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.castable import conductivity_law

    law = conductivity_law()
    held_out = {
        "Firelite 2600LI": ("[M24]", 1140, ((200, 0.38), (400, 0.38), (600, 0.38), (800, 0.39),
                                            (1000, 0.39))),
        "Kaolite 2600LI Pump": ("[M20]", 1201, ((260, 0.39), (538, 0.42), (816, 0.43),
                                                (1093, 0.46))),
        "Kaolite 2600LI Gun": ("[M21]", 1250, ((260, 0.42), (538, 0.42), (816, 0.43),
                                               (1093, 0.46))),
    }  # fmt: skip
    results = []
    for name, (source, density, points) in held_out.items():
        for t, k in points:
            results.append(
                compare(f"{name}, {t} °C, W/(m·K)", f"Morgan {source}", law.k(density, t + 273.15),
                        k, 0.25)
            )  # fmt: skip
    # The band the results quote is the held-out band seen here
    errors = [r["error"] for r in results[:9]]
    results += [
        compare("quoted band, low", "Firelite and Kaolite Pump", law.held_out[0], min(errors), 1e-9,
                absolute=True),
        compare("quoted band, high", "Firelite and Kaolite Pump", law.held_out[1], max(errors),
                1e-9, absolute=True),
    ]  # fmt: skip
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
