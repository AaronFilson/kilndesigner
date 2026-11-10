"""Target times (problem set §2.2; `thermal-software.md` §12): how long a fixed input takes to
bring the setting to a temperature, one firing stopped by IDA's event; and the input that takes a
given time, a root of that found by Brent's method around whole firings (SciPy's `brentq`, through
`numeric.find_root`).

A stoked kiln's time is the stoker's choice within its draft's air (`firing.MaxFire` bounds it);
here the input is a steady fuel rate either way: burners at a setting, or a steady stoking rate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from kilndesigner.numeric import find_root
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat.zone import ZoneModel
from kilndesigner.working import Step


class TargetError(ValueError):
    """No input in the range tried reaches the target in the time (a refusal with its reason)."""


@dataclass(frozen=True)
class Target:
    """The fuel rate (kg/s) that brings the setting to ``temperature`` (K) in ``time`` (s)."""

    fuel: float
    time: float
    temperature: float
    firings: int
    steps: tuple[Step, ...] = field(default=())


def time_at(model: ZoneModel, fuel: float, temperature: float, t_max: float) -> float | None:
    """When the setting reaches ``temperature`` at a steady fuel rate (s), or None by t_max."""
    f = fi.fire(model, fi.FixedInput(fuel), t_max, (), temperature, sample=600.0)
    return f.reached(temperature)


def input_for(
    model: ZoneModel,
    temperature: float,
    time: float,
    guess: float,
    most: float = 8.0,
    tol: float = 0.002,
) -> Target:
    """The steady fuel rate that reaches ``temperature`` (K) in ``time`` (s), from ``guess``
    (kg/s), searched between guess/most and guess·most; ``tol`` the time's relative tolerance."""
    seen: dict[float, float] = {}

    def miss(f: float) -> float:
        if f not in seen:
            t = time_at(model, f, temperature, 3 * time)
            seen[f] = (3 * time if t is None else t) / time - 1.0
        return seen[f]

    lo, hi = guess, guess
    while miss(hi) > 0:
        hi *= 2.0
        if hi > guess * most:
            raise TargetError(
                f"{temperature - 273.15:.0f} °C isn't reached in {time / 3600:.1f} h even at "
                f"{most:g} times the input tried ({guess * most:.5f} kg/s)"
            )
    while miss(lo) < 0:
        lo /= 2.0
        if lo < guess / most:
            raise TargetError(
                f"{temperature - 273.15:.0f} °C is reached in under {time / 3600:.1f} h even at "
                f"1/{most:g} of the input tried"
            )
    fuel = find_root(miss, lo, hi, xtol=tol * lo)
    step = Step(
        name="The input for the time",
        value=f"{fuel:.6f} kg/s brings the setting to {temperature - 273.15:.0f} °C in "
        f"{time / 3600:.2f} h ({fuel / guess:.3f} × the input tried first)",
        formula="t(F) = time, Brent's method around whole firings (IDA's event)",
        inputs={
            "firings": str(len(seen)),
            "net heat": f"{fuel * model.products.net_heat / 1e3:.1f} kW",
        },
        reference="SciPy brentq (numeric.find_root); thermal-software.md §12",
    )
    return Target(fuel, time, temperature, len(seen), (step,))
