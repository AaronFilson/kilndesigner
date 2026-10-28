"""Low-pressure (3-11 in w.c.) partly premixed venturi burner against the chimney's suction.

A plain pipe burner: no diffuser, and the mixture leaves the tip losing K_EXIT velocity heads.
Suction at the tip (from the chimney) adds to what the gas jet pulls in. Also: secondary air
through the port gap, chimney suction at the top and floor ports, and the 9 x 9 in flue's loss.

Run: python3 docs/top-down/models/low_pressure.py
"""

import math

import inspirator as m

PIPE = {**m.REAL, "eta_d": 0.0}  # straight pipe burner: no diffuser recovery
K_EXIT = 1.5  # exit velocity head plus retention tip, assumed


def primary(
    p_s: float, d_j_in: float, d_t_in: float, suction: float, k_extra: float = 0.0
) -> tuple[float, float]:
    """Primary air (fraction of stoichiometric) and tube velocity for tip suction in Pa."""
    alpha = (d_t_in / d_j_in) ** 2

    def resid(r: float) -> float:
        p2, v_m, rho_m = m.mixer(p_s, r, alpha, PIPE)
        return p2 + suction - (K_EXIT + k_extra) * 0.5 * rho_m * v_m**2

    lo, hi = 0.05, 40.0
    if resid(lo) < 0:
        return 0.0, 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if resid(mid) > 0:
            lo = mid
        else:
            hi = mid
    _, v_m, _ = m.mixer(p_s, lo, alpha, PIPE)
    return lo / m.R_ST, v_m


def orifice_cfh(d_in: float, inwc: float) -> float:
    """Propane flow, ft3/h, from the orifice equation in combustion-and-masonry.md section 3.4."""
    return 1658.5 * math.pi / 4 * d_in**2 * 0.9 * math.sqrt(inwc / 1.522)


def main() -> None:
    d_j = 0.039  # #61 drill; the proposed design uses #59 (0.041 in)
    for name, d_t in (
        ("3/8 in Sch 40 (0.493 in ID)", 0.493),
        ("1/2 in Sch 40 (0.622 in ID)", 0.622),
    ):
        print(f"\n#61 orifice, {name}, area ratio {(d_t / d_j) ** 2:.0f}")
        for ps in (3, 7, 11):
            row = [f"{primary(ps * m.INWC, d_j, d_t, s)[0] * 100:4.0f}%" for s in (0, 3, 8, 13, 19)]
            print(
                f"  {ps:2d} in w.c.: {orifice_cfh(d_j, ps) * m.HHV_FT3:6.0f} BTU/hr | "
                f"primary air at 0/3/8/13/19 Pa suction: {' '.join(row)}"
            )
        a, v = primary(11 * m.INWC, d_j, d_t, 0.0)
        elbow, _ = primary(11 * m.INWC, d_j, d_t, 0.0, k_extra=0.9)
        bend, _ = primary(11 * m.INWC, d_j, d_t, 0.0, k_extra=0.25)
        print(
            f"  11 in, no suction: tube {v:.1f} m/s; air {a * 100:.0f} % straight, "
            f"{elbow * 100:.0f} % with a threaded 90, {bend * 100:.0f} % with a long-radius bend"
        )

    for drill, d in (("#61", 0.039), ("#59", 0.041), ("#57", 0.043)):
        out = [f"{orifice_cfh(d, ps) * m.HHV_FT3:6.0f}" for ps in (3, 7, 11)]
        print(f"{drill} ({d} in): BTU/hr at 3/7/11 in w.c. = {' / '.join(out)}")

    ann = math.pi / 4 * (1.5**2 - 0.84**2) * 0.0254**2  # 1.5 in port around 1/2 in pipe
    gas_m3s = 12_000 / m.HHV_FT3 / 3600 * 0.0283168
    for s in (3, 8):
        air = 0.6 * math.sqrt(2 * s / m.RHO_A) * ann
        print(
            f"port gap {ann * 1e6:.0f} mm2 at {s} Pa passes {air * 1000:.2f} L/s = "
            f"{air / (gas_m3s * m.VOL_ST) * 100:.0f} % of a 12,000 BTU/hr burner's air"
        )

    rho_k = m.RHO_A * 293.15 / (1285 + 273.15)
    print("\nSuction at the ports (kiln 0.72 m tall at 1285 C; friction ~0.5 Pa):")
    for t_ch in (500, 700, 900):
        rho_c = m.RHO_A * 293.15 / (t_ch + 273.15)
        for h_ft in (4, 6, 8, 10):
            draft = (m.RHO_A - rho_c) * 9.81 * h_ft * 0.3048
            top = -draft + (m.RHO_A - rho_k) * 9.81 * 0.72 + 0.5
            bot = -draft + (m.RHO_A - rho_k) * 9.81 * 0.05 + 0.4
            print(
                f"  chimney {h_ft:2d} ft, {t_ch} C mean: top {top:+5.1f} Pa, floor {bot:+5.1f} Pa"
            )

    mdot = 26_000 / 50.12e6 * (1 + m.R_ST * 1.15)  # 26 kW gross, 15 % excess air
    rho_h = m.RHO_A * 293.15 / 1558.15
    vol = mdot / rho_h
    v = vol / (81 * 0.0254**2)
    print(
        f"hot gas {vol * 1000:.0f} L/s; 9x9 flue {v:.2f} m/s, velocity head "
        f"{0.5 * rho_h * v**2:.2f} Pa"
    )


if __name__ == "__main__":
    main()
