"""Validation: the steady layered-wall solver against published worked examples (ADR 0009)."""

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
    # Layered-wall heat loss (`kilndesigner.thermal.wall`)

    The steady solver against three published multi-layer walls, all from
    `docs/research/electric-and-thermal.md` §6.4:

    - **A.** FOSSEE, *Basic Mechanical Engineering*, Example 6.11, p.232 [S64]: fire brick
      0.2 m (k 4.0) and common brick 0.2 m (k 0.65), gas at 1400 °C with h = 34, air at 50 °C with
      h = 19. Published: 3.07 kW/m², hot face 1309.705 °C, interface 1156.204 °C.
    - **B.** The same book, Example 6.5, p.226 [S64], given in kJ/h (÷ 3.6 for W). Published:
      5916.3 kJ/(h·m²), inner surface 1625.88 °C, outer surface 171.72 °C.
    - **C.** CSJM University, CHE S204 ch. 2 [S65]: three layers between faces at 870 °C and
      40 °C. The source gives the resistances and stops before the answer, so its 837.0 W/m² and
      interfaces 685.9 °C and 162.8 °C are worked from the source's own resistances (derived).

    Tolerance: 0.1 % on the heat flow (the books print 3–5 figures) and 0.1 K on temperatures.

    **Not sourced, so not checked:** an ASTM C680 worked example (3E Plus runs C680 but publishes no
    worked cases), and a kiln-specific IFB + fibre + steel wall with numbers. Olsen's Table 1-12
    (p.39) gives no ambient or method, so it is recorded in `kiln-reference.md`, not tested here.
    """)
    return


@app.cell
def _(compare):
    from kilndesigner.thermal.conductivity import Conductivity
    from kilndesigner.thermal.surface import FixedSurface
    from kilndesigner.thermal.wall import Slab, solve_wall

    C = 273.15  # noqa: N806 (°C to K, as in the tests)

    def slab(name, thickness, k):
        return Slab(name, thickness, Conductivity.constant(k))

    a = solve_wall(
        [slab("fire brick", 0.2, 4.0), slab("common brick", 0.2, 0.65)],
        1400 + C,
        50 + C,
        FixedSurface(19.0),
        inside_coefficient=34.0,
    )
    b = solve_wall(
        [slab("brick", 0.225, 4.984 / 3.6), slab("insulating brick", 0.125, 0.623 / 3.6)],
        1650 + C,
        27 + C,
        FixedSurface(40.88 / 3.6),
        inside_coefficient=245.28 / 3.6,
    )
    c = solve_wall(
        [slab("fire brick", 0.22, 1.0), slab("insulating", 0.075, 0.12), slab("red", 0.11, 0.75)],
        870 + C,
        40 + C,
        FixedSurface(1e9),  # pins the outside face to 40 °C
    )
    fossee, csjm = "FOSSEE [S64]", "CSJM [S65], from its resistances"
    results = [
        compare("A: heat flow, W/m²", fossee, a.heat_flow, 3070, 1e-3),
        compare("A: hot face, °C", fossee, a.hot_face - C, 1309.705, 0.1, absolute=True),
        compare("A: interface, °C", fossee, a.interfaces[0] - C, 1156.204, 0.1, absolute=True),
        compare("B: heat flow, kJ/(h·m²)", fossee, b.heat_flow * 3.6, 5916.3, 1e-3),
        compare("B: inner surface, °C", fossee, b.hot_face - C, 1625.88, 0.1, absolute=True),
        compare("B: outer surface, °C", fossee, b.surface - C, 171.72, 0.1, absolute=True),
        compare("C: heat flow, W/m²", csjm, c.heat_flow, 837.0, 1e-3),
        compare("C: first interface, °C", csjm, c.interfaces[0] - C, 685.9, 0.1, absolute=True),
        compare("C: second interface, °C", csjm, c.interfaces[1] - C, 162.8, 0.1, absolute=True),
    ]
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
