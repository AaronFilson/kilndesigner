"""First-principles model of a gas-jet inspirator (venturi mixer) on propane.

One-dimensional control volume:
- gas nozzle: isentropic and compressible, choking above about 10.6 psig;
- bell-mouth air inlet: loses K_IN of the air's velocity head;
- constant-area mixing tube: momentum balance, loses K_MIX of the mixed velocity head;
- conical diffuser: recovers ETA_D of the mixed velocity head (0 for a plain pipe burner);
- manifold or burner head, then the ports.

`best` optimises the throat-to-orifice area ratio for each air-to-gas ratio, so its result is an
upper bound for any geometry with these losses. The loss coefficients are assumptions, not
measurements. Propane data come from docs/research/combustion-and-masonry.md section 1.1.

Run: python3 docs/top-down/models/inspirator.py
"""

import math

P_ATM = 101_325.0
T0 = 293.15
R_U = 8.314
M_C3H8 = 0.04410
M_AIR = 0.02896
K_C3H8 = 1.13  # ratio of specific heats, as in combustion-and-masonry.md section 3.4
RHO_A = P_ATM * M_AIR / (R_U * T0)  # 1.204 kg/m3
RHO_G0 = P_ATM * M_C3H8 / (R_U * T0)  # 1.83 kg/m3 at 1 atm
R_ST = 15.67  # stoichiometric air/fuel by mass (section 1.1, derived)
VOL_ST = 23.86  # ft3 air per ft3 propane (section 1.1 [S1])
HHV_FT3 = 2488.0  # BTU/ft3 (section 1.1 [S1])
INWC = 249.089  # Pa per inch of water
PSI = 6894.76

REAL = {"cd": 0.90, "cv": 0.96, "k_in": 0.05, "k_mix": 0.15, "eta_d": 0.80}
IDEAL = {"cd": 1.0, "cv": 1.0, "k_in": 0.0, "k_mix": 0.0, "eta_d": 1.0}


def nozzle(p_s: float, p_back: float, cd: float, cv: float) -> tuple[float, float, float]:
    """Mass flux (kg/s per m2 of orifice), thrust (N per m2) and jet velocity for gauge p_s."""
    p0 = P_ATM + p_s
    pb = P_ATM + p_back
    k = K_C3H8
    rho0 = p0 * M_C3H8 / (R_U * T0)
    crit = (2 / (k + 1)) ** (k / (k - 1))
    pe = max(pb, crit * p0)
    ratio = pe / p0
    v = math.sqrt(2 * k / (k - 1) * p0 / rho0 * (1 - ratio ** ((k - 1) / k)))
    rho_e = rho0 * ratio ** (1 / k)
    g = cd * rho_e * v
    thrust = g * cv * v + (pe - pb)  # pressure thrust of an under-expanded (choked) jet
    return g, thrust, cv * v


def mixer(p_s: float, r: float, alpha: float, c: dict[str, float]) -> tuple[float, float, float]:
    """Gauge pressure delivered downstream, mixed velocity and mixture density.

    r is air/gas by mass; alpha is throat area / orifice area. Returns a large negative pressure
    when the throat suction runs away, meaning this (r, alpha) pair has no solution.
    """
    p1 = 0.0
    for _ in range(200):
        g, _, _ = nozzle(p_s, p1, c["cd"], c["cv"])
        v_a = r * g / (RHO_A * (alpha - 1))
        p1_new = -0.5 * RHO_A * v_a**2 * (1 + c["k_in"])
        if p1_new < -0.03 * P_ATM:
            return -1e9, 0.0, 0.0
        if abs(p1_new - p1) < 1e-9:
            p1 = p1_new
            break
        p1 = p1_new
    else:
        return -1e9, 0.0, 0.0
    g, thrust, _ = nozzle(p_s, p1, c["cd"], c["cv"])
    m_a = r * g
    v_a = m_a / (RHO_A * (alpha - 1))
    rho_m = (1 + r) / (1 / RHO_G0 + r / RHO_A)
    m_m = (1 + r) * g
    v_m = m_m / (rho_m * alpha)
    q_m = 0.5 * rho_m * v_m**2
    p2 = p1 + (thrust + m_a * v_a - m_m * v_m) / alpha - c["k_mix"] * q_m
    return p2 + c["eta_d"] * q_m, v_m, rho_m


def best(p_s: float, r: float, c: dict[str, float]) -> tuple[float, float]:
    """Highest delivered pressure over all area ratios, and the area ratio that gives it."""
    top, top_alpha = -1e9, 0.0
    alpha = 2.0
    while alpha < 50_000:
        p3, _, _ = mixer(p_s, r, alpha, c)
        if p3 > top:
            top, top_alpha = p3, alpha
        alpha *= 1.02
    return top, top_alpha


def max_aeration(p_s: float, p_req: float, c: dict[str, float]) -> float:
    """Largest fraction of stoichiometric air the best geometry can deliver at p_req."""
    lo, hi = 0.1, 40.0
    if best(p_s, lo, c)[0] < p_req:
        return 0.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if best(p_s, mid, c)[0] >= p_req:
            lo = mid
        else:
            hi = mid
    return lo / R_ST


def supply_for_full(p_req: float, c: dict[str, float]) -> float:
    """Gas supply pressure (Pa gauge) the best geometry needs to deliver p_req at 100 % air."""
    lo, hi = 10.0, 60 * PSI
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if best(mid, R_ST, c)[0] >= p_req:
            hi = mid
        else:
            lo = mid
    return hi


def port_head(v: float, cd: float = 0.8) -> float:
    """Pressure to push a stoichiometric mixture out of a port at v m/s."""
    rho_m = (1 + R_ST) / (1 / RHO_G0 + R_ST / RHO_A)
    return 0.5 * rho_m * (v / cd) ** 2


def fmt_p(p: float) -> str:
    return f"{p / INWC:6.2f} in w.c." if p < 2 * PSI else f"{p / PSI:5.1f} psi"


def design(btu_hr_each: float, v_port: float, extra_pa: float, port_id_mm: float, ports: int):
    """Size one inspirator feeding one half-ring manifold of `ports` ports."""
    p_req = port_head(v_port) + extra_pa
    p_s = supply_for_full(p_req, REAL)
    p3, alpha = best(p_s, R_ST, REAL)
    _, v_m, rho_m = mixer(p_s, R_ST, alpha, REAL)
    m_g = btu_hr_each / 21_548 * 0.453592 / 3600  # HHV 21,548 BTU/lb, section 1.1 [S1]
    g, _, _ = nozzle(p_s, 0.0, REAL["cd"], REAL["cv"])
    d_j = math.sqrt(4 * (m_g / g) / math.pi)
    q_mix = m_g * (1 + R_ST) / rho_m
    a_each = math.pi / 4 * (port_id_mm / 1000) ** 2
    return {
        "p_s": p_s,
        "p3": p3,
        "alpha": alpha,
        "d_j": d_j,
        "d_t": d_j * math.sqrt(alpha),
        "v_throat": v_m,
        "q_mix": q_mix,
        "v_actual": q_mix / (ports * a_each),
        "port_area_total": ports * a_each,
    }


def main() -> None:
    rho_m = (1 + R_ST) / (1 / RHO_G0 + R_ST / RHO_A)
    print(f"rho air {RHO_A:.3f}, propane {RHO_G0:.3f}, stoichiometric mix {rho_m:.3f} kg/m3")
    rho_h = RHO_A * T0 / (1250 + 273.15)
    stack = (RHO_A - rho_h) * 9.81 * 0.75
    print(f"buoyancy head over 0.75 m at 1250 C: {stack:.1f} Pa = {stack / INWC:.3f} in w.c.")

    print("\nDelivered pressure at 100 % primary air (best geometry):")
    for label, c in (("real losses", REAL), ("no losses", IDEAL)):
        for ps_in in (3, 7, 11):
            p3, a = best(ps_in * INWC, R_ST, c)
            v = 0.8 * math.sqrt(2 * max(p3, 0) / rho_m)
            print(
                f"  {label:11s} {ps_in:2d} in w.c.: {p3:6.2f} Pa (area ratio {a:4.0f}), "
                f"ports {v:.2f} m/s with no back pressure"
            )

    print("\nEnergy bound for any mixer at 100 % air: p_manifold <= p_supply / 24.86")
    for ps_in in (3, 7, 11):
        print(f"  {ps_in:2d} in w.c. -> {ps_in * INWC / (1 + VOL_ST):5.1f} Pa")

    print("\nMost primary air the best geometry delivers (fraction of stoichiometric):")
    cases = (
        ("ports 2.5 m/s, buoyancy cancelled", port_head(2.5)),
        ("ports 5 m/s, buoyancy cancelled", port_head(5)),
        ("ports 10 m/s, buoyancy cancelled", port_head(10)),
        ("ports 10 m/s, no stack, flue 3 Pa", port_head(10) + stack + 3),
    )
    for label, p_req in cases:
        row = [f"{max_aeration(ps * INWC, p_req, REAL) * 100:4.0f}%" for ps in (3, 7, 11)]
        print(f"  {label:35s} ({p_req:5.1f} Pa): 3 in {row[0]}, 7 in {row[1]}, 11 in {row[2]}")

    print("\nSupply pressure for 100 % primary air:")
    for v in (5, 10, 15, 20):
        p_req = port_head(v)
        print(
            f"  ports {v:2d} m/s ({p_req:5.1f} Pa): {fmt_p(supply_for_full(p_req, REAL))} "
            f"(no-loss bound {fmt_p(supply_for_full(p_req, IDEAL))})"
        )

    print("\nFull-premix design: 2 inspirators x 50,000 BTU/hr, each feeding a half-ring of")
    print("10 ports of 5/16 in OD x 0.035 in tube (6.16 mm ID); stack cancels buoyancy; flue 3 Pa")
    d = design(50_000, 13.3, 3.0, 6.16, 10)
    print(
        f"  supply {fmt_p(d['p_s'])}, manifold {d['p3']:.0f} Pa, orifice {d['d_j'] * 1000:.2f} mm "
        f"({d['d_j'] / 0.0254:.4f} in), best throat {d['d_t'] * 1000:.1f} mm, "
        f"mix {d['q_mix'] * 1000:.2f} L/s, ports {d['v_actual']:.1f} m/s"
    )
    for f in (1.0, 0.7, 0.5, 0.3):
        print(
            f"    {f * 100:3.0f} % flow: supply {fmt_p(d['p_s'] * f**2)}, "
            f"ports {d['v_actual'] * f:4.1f} m/s"
        )
    need = port_head(13.3) + 3.0
    print(f"  Throat choice at that supply ({need:.0f} Pa needed):")
    for dt_mm, label in ((12.0, "12 mm"), (15.8, "1/2 in Sch 40"), (20.9, "3/4 in Sch 40")):
        p3, _, _ = mixer(d["p_s"], R_ST, (dt_mm / (d["d_j"] * 1000)) ** 2, REAL)
        print(f"    {label:14s}: {p3:6.1f} Pa")
    for label, c in (
        ("diffuser 70 %", {**REAL, "eta_d": 0.7}),
        ("sharp air inlet", {**REAL, "k_in": 0.5}),
        ("mixing loss 0.3", {**REAL, "k_mix": 0.3}),
    ):
        print(f"    {label:16s}: air {max_aeration(d['p_s'], need, c) * 100:.0f} % of needed")

    print("\nManifold uniformity (port flow ~ sqrt of local pressure):")
    for name, id_mm in (("1 in Sch 40", 26.64), ("1-1/4 in Sch 40", 35.05)):
        a_man = math.pi / 4 * (id_mm / 1000) ** 2
        for feed, share in (("end-fed", 1.0), ("centre-fed", 0.5)):
            v_man = d["q_mix"] * share / a_man
            spread = 0.5 * (0.5 * rho_m * v_man**2) / port_head(d["v_actual"])
            print(
                f"  {name:15s} {feed:10s}: {v_man:4.1f} m/s, "
                f"{a_man / d['port_area_total']:.1f}x port area, spread ~{spread * 100:.1f} %"
            )

    print("\nMizzou ring cold face, 1250 C hot face, k 1.12 W/mK (electric-and-thermal.md 4.5):")
    for t_in in (3.0, 4.5):
        for h in (20, 35):
            q = (1250 - 20) / (t_in * 0.0254 / 1.12 + 1 / h)
            print(
                f"  {t_in} in, outside h {h} W/m2K: {q / 1000:4.1f} kW/m2, "
                f"cold face {20 + q / h:4.0f} C"
            )


if __name__ == "__main__":
    main()
