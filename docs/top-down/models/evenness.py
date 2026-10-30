"""Top-to-bottom spread at soak for the 23 in, 27 in tall, 2.5 in K-23 kiln, by where heat goes in.

Lumped model: five gas spaces stacked between four shelves (S0 at the floor to S4 under the lid).
Hot gas sheds its excess heat in the first space it enters: gas-to-surface coupling of 50-100 W/K
per space against the burner flow's ~13 W/K. So heat goes in where the burners fire. It then moves
between spaces through each shelf by radiation and shelf conduction (G_R, estimated, not
measured), plus the enthalpy the descending through-flow carries (mdot * cp).

Run: python3 docs/top-down/models/evenness.py
"""

import math

T_HOT = 1285.0  # cone 10 at 60 C/h (core/src/kilndesigner/data/cones.yaml)
K_IFB = 0.195  # W/mK: K-23 near 760 C mean, 1.35 Btu.in/h.ft2.F (electric-and-thermal.md 4.1)
WALL = 2.5 * 0.0254
H_OUT = 15.0  # W/m2K outside, assumed
MCP_ALL = 12.8  # W/K: products of ~26 kW gross propane at ~15 % excess air
BANDS_IN = (3, 6, 6, 6, 6)  # heights of S0..S4


def perimeter(across_flats_in: float) -> float:
    return 10 * across_flats_in * math.tan(math.radians(18)) * 0.0254


def losses() -> list[float]:
    q = (T_HOT - 20) / (WALL / K_IFB + 1 / H_OUT)
    side_per_m = (perimeter(23) + perimeter(28)) / 2 * q
    slab = 0.8123 * ((23 + 28) / 2 * 0.0254) ** 2 * q  # lid or floor, mean area
    out = [side_per_m * b * 0.0254 for b in BANDS_IN]
    out[0] += slab
    out[4] += slab
    return out


def spread(loss: list[float], f_top: float, g_r: float, recirc: float = 0.0) -> list[float]:
    """Temperatures of S0..S4 relative to S4, with f_top of the heat entering at the top."""
    q_top = f_top * sum(loss)
    mcp = f_top * MCP_ALL * (1 + recirc)
    temps = [0.0]
    above = 0.0
    for k in range(4, 0, -1):  # the shelf between S_k and S_(k-1)
        above += loss[k]
        temps.append(temps[-1] - (q_top - above) / (g_r + mcp))
    return temps[::-1]


def balanced(loss: list[float], g_r: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if spread(loss, mid, g_r)[0] < 0:
            hi = mid
        else:
            lo = mid
    return lo


def main() -> None:
    loss = losses()
    print(f"losses S0..S4 (kW): {[round(x / 1000, 2) for x in loss]}, total {sum(loss) / 1000:.2f}")
    for label, g in (("SiC shelves, G_r 85 W/K", 85.0), ("cordierite shelves, G_r 50 W/K", 50.0)):
        print(f"\n{label}")
        f_bal = balanced(loss, g)
        cases = (
            ("top ring only", 1.0, 0.0),
            ("top only, 5x recirculation", 1.0, 5.0),
            ("70 % top / 30 % bottom", 0.7, 0.0),
            (f"{f_bal * 100:.0f} % top / {100 - f_bal * 100:.0f} % bottom (balanced)", f_bal, 0.0),
        )
        for name, f, rc in cases:
            t = spread(loss, f, g, rc)
            print(
                f"  {name:40s}: bottom vs top {t[0]:+5.0f} K, "
                f"coolest {min(t):+5.0f} K, spread {max(t) - min(t):4.0f} K"
            )


if __name__ == "__main__":
    main()
