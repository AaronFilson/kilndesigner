"""Two MR-100s sealed into the lid, firing straight down at 11 in w.c.

1. With the lid sealed, all the air comes through the venturis. How much suction at the tip
   gives a given air ratio?
2. Leak air through gaps in the kiln at a given suction.
3. Does a straight-down jet reach the floor? A buoyant jet fired against its buoyancy, by
   fountain scaling: penetration about 1.85-2.46 * M^(3/4) / B^(1/2). The coefficients are
   textbook (Turner) and not yet in docs/research.

Run: python3 docs/top-down/models/sealed_lid.py
"""

import math

import inspirator as m
import low_pressure as lp


def orifice_for(btu: float, inwc: float) -> float:
    a = btu / m.HHV_FT3 / (1658.5 * 0.9 * math.sqrt(inwc / 1.522))
    return math.sqrt(4 * a / math.pi)


def suction_for(lam: float, p_s: float, d_j: float, d_t: float) -> float:
    lo, hi = -50.0, 2000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if lp.primary(p_s, d_j, d_t, mid)[0] < lam:
            lo = mid
        else:
            hi = mid
    return hi


def main() -> None:
    print(f"rich limit: 9.6 % propane in air -> lambda {(90.4 / 9.6) / m.VOL_ST:.3f}")
    p11 = 11 * m.INWC
    for btu, label in ((94_000, "Ward's 11 in rating"), (50_000, "what this kiln needs")):
        d_j = orifice_for(btu, 11)
        for name, d_t in (("1 in Sch 40", 1.049), ("3/4 in Sch 40", 0.824)):
            a0, _ = lp.primary(p11, d_j, d_t, 0.0)
            s90 = suction_for(0.9, p11, d_j, d_t)
            s105 = suction_for(1.05, p11, d_j, d_t)
            print(
                f"{btu:6d} BTU/hr ({label}), orifice {d_j:.3f} in, {name}: "
                f"air {a0 * 100:.0f} % with no draft; suction for 90 %: {s90:.0f} Pa, "
                f"for 105 %: {s105:.0f} Pa"
            )

    stoich_100k = 100_000 / m.HHV_FT3 * m.VOL_ST / 3600 * 0.0283168  # m3/s of air
    for s in (15, 60):
        per_in2 = 0.6 * math.sqrt(2 * s / m.RHO_A) * 0.0254**2
        print(
            f"leak at {s} Pa: {per_in2 * 1000:.1f} L/s per in2 of gap = "
            f"{per_in2 / stoich_100k * 100:.0f} % of the air for 100,000 BTU/hr"
        )

    rho_k = m.RHO_A * 293.15 / 1558.15
    for label, v in (("11 in w.c. gas jet", None), ("blower air, 20 m/s tip", 20.0)):
        fuel = 50_000 / 21_548 * 0.453592 / 3600
        flow = fuel * (1 + m.R_ST * 1.05)
        if v is None:
            _, _, vj = m.nozzle(p11, 0.0, 0.9, 0.96)
            j = fuel * vj
        else:
            j = flow * v
        b = 9.81 * flow * 1300 * 500 / (rho_k * 1300 * 1558.15)  # products ~500 K over the kiln
        lm = (j / rho_k) ** 0.75 / b**0.5
        print(
            f"{label}: momentum {j * 1000:.1f} mN, Morton length {lm:.2f} m, "
            f"penetration ~{1.85 * lm:.2f}-{2.46 * lm:.2f} m (kiln ~0.69 m deep)"
        )


if __name__ == "__main__":
    main()
