"""Validation: chimney height and draft against Olsen's and Ward's worked examples."""

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
    # Chimney draft (`kilndesigner.fire`, `kilndesigner.gas`)

    - **Olsen's Rule 5** (*The Kiln Book*, 4th ed., p.79–80, Fig. 3-14; `olsen-kilns.md` W7): a
      chamber 5 ft along the draft and 6 ft to the crown, 1 ft of flue box, a chimney 1 ft across.
      3 × 6 ft + (5 + 1 + 1) ÷ 3 ft = **20 ft 4 in** (244 in). The engine's most, built with no
      chimney height given in the design, must be 244 in. Tolerance 0.5 in.
    - **Ward's worked example** (`combustion-and-masonry.md` §4.1 [S32]): 36 in inside height and
      54 in of linear draw (36 in deep + 9 in back wall + 9 in to the chimney's base):
      3 × 36 + 54/3 = **126 in**. Ward stops at the chimney's base; Olsen (and the engine) also
      count the chimney's own width (here 9 in, so 129 in). Tolerance 3 %, for that difference of
      definition.
    - **Air at altitude**: Ward's burner factor, printed by Olsen, 0.9279 at 5000 ft (p.230) and
      0.8579 at 10,000 ft (p.232), against the engine's √(ρ/ρ₀) from NASA's atmosphere model
      (§4.3 [S88]). Tolerance 0.5 %.
    - **The stack-effect draft**: the engine's SI form ΔP = 0.0342·a·h·(1/T_o − 1/T_i) [S42]
      against Wikipedia's US form, 0.0188·a(psia)·h(ft)·(1/T_o − 1/T_i)(°R) psi [S80], at
      27.7 in. w.c. per psi (§2.7 [S21]). The two published forms agree to 0.3 %; the engine
      prints the draft to 0.001 in. w.c. Tolerance 1 %.

    **Not sourced, so not checked:** a measured draft on a real kiln chimney.
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.fire import design_fire
    from kilndesigner.gas import altitude_factor
    from kilndesigner.model import Kiln
    from kilndesigner.units import si

    def kiln(height, depth, run, chimney_inside):
        inside = f"{chimney_inside} in"
        return Kiln.model_validate(
            {
                "name": "chimney example",
                "firing": {"cone": "10"},
                "chamber": {"width": "48 in", "depth": f"{depth} in", "height": f"{height} in"},
                "lining": {"walls": [{"material": "hard-firebrick-kx99", "thickness": "9 in"}]},
                "heat": {
                    "fire": {
                        "fuel": "wood",
                        "fireboxes": [
                            {
                                "width": "48 in",
                                "length": "36 in",
                                "grate": {"width": "48 in", "length": "30 in"},
                            }
                        ],
                    }
                },
                "draft": {
                    "type": "cross",
                    "run_to_chimney": f"{run} in",
                    "chimney": {"height": "244 in", "inside": {"width": inside, "depth": inside}},
                },
            }
        )

    def most(fire):
        assert fire.chimney_range is not None
        return float(fire.chimney_range.split("–")[1].split()[0]) * 12

    # Olsen: 60 in along the draft, a 1 ft flue box (the 9 in flue wall and a 3 in run) and a
    # chimney 12 in across. Ward: 36 in deep, a 9 in back wall, 9 in to the chimney's base.
    olsen = design_fire(kiln(72, 60, 3, 12))
    ward = design_fire(kiln(36, 36, 9, 9))
    results = [
        compare("Olsen Rule 5, most, in", "Olsen p.80, W7", most(olsen), 244, 0.5 / 244),
        compare("Ward, 3H + L/3, in", "Ward [S32]", most(ward), 126, 0.03),
        compare("altitude factor, 5000 ft", "Ward via Olsen p.230", altitude_factor(1524), 0.9279,
                0.005),
        compare("altitude factor, 10,000 ft", "Ward via Olsen p.232", altitude_factor(3048), 0.8579,
                0.005),
    ]  # fmt: skip

    # The draft at the base of Olsen's 244 in chimney with flue gas at 1000 °F
    k = kiln(72, 60, 3, 12)
    to_r = si(k.site.ambient, "degR")
    us_form = 0.0188 * 14.696 * (244 / 12) * (1 / to_r - 1 / (1000 + 459.67)) * 27.7
    engine = float(olsen.draft[0].split()[0])
    results.append(compare("draft, flue 1000 °F, in. w.c.", "Wikipedia US form [S80]", engine,
                           us_form, 0.01))  # fmt: skip
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
