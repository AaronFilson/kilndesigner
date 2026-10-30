"""Validation: the finite-volume transient wall against the heated-slab erf solution."""

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
    # Transient wall (`kilndesigner.thermal.transient`)

    A thick slab (k 1 W/mK, ρ 2000 kg/m³, c 1000 J/kgK) at 300 K whose face steps to 1300 K and is
    held there for an hour. The published solution for a semi-infinite solid is
    T = T_s + (T_i − T_s)·erf(x / 2√(αt)) (Holman, *Heat Transfer*, eq. 4-8), and the heat taken
    in, the integral of eq. 4-12, Q/A = 2k(T_s − T_i)√(t/πα) (`thermal-properties.md` §8.3
    [T45]).

    Tolerance: 1 K (0.1 % of the step) on the temperatures through the first 0.15 m, and 0.1 % on
    the heat. Backward Euler's first steps after the sudden jump are the main error (about 0.2 K
    and 0.02 % with 1 mm cells and 5 s steps).

    **Not sourced, so not checked:** a published transient kiln-wall case (a firing schedule with
    measured or published face temperatures).
    """)
    return


@app.cell
def _(compare):
    import math

    from kilndesigner.thermal.conductivity import Conductivity
    from kilndesigner.thermal.surface import FixedSurface
    from kilndesigner.thermal.transient import HeatCapacity, Layer, TransientWall

    k, rho, c = 1.0, 2000.0, 1000.0
    alpha = k / (rho * c)
    layer = Layer("slab", 0.5, Conductivity.constant(k), rho, HeatCapacity.constant(c))
    wall = TransientWall([layer], FixedSurface(0.0), 300.0, 300.0, max_cell=0.001)
    seconds, dt = 3600.0, 5.0
    heat_in = 0.0
    for _ in range(round(seconds / dt)):
        out = wall.prepare(dt)(1300.0)
        wall.commit(1300.0, out.surface)
        heat_in += out.heat_in

    holman = "Holman eq. 4-8, §8.3 [T45]"
    results = []
    for x_mm in (5, 20, 50, 100, 150):
        x = x_mm / 1000
        i = min(range(len(wall.centres)), key=lambda j: abs(wall.centres[j] - x))
        xc = wall.centres[i]
        exact = 1300.0 + (300.0 - 1300.0) * math.erf(xc / (2 * math.sqrt(alpha * seconds)))
        results.append(
            compare(f"T at {xc * 1000:.1f} mm, K", holman, wall.temperatures[i], exact, 1.0,
                    absolute=True)
        )  # fmt: skip
    exact_q = 2 * k * 1000.0 * math.sqrt(seconds / (math.pi * alpha))
    results.append(compare("heat in an hour, J/m²", "Holman eq. 4-12", heat_in, exact_q, 1e-3))
    return (results,)


@app.cell
def _(markdown, mo, results):
    mo.md(markdown(results))
    return


if __name__ == "__main__":
    app.run()
