"""Checks as sheets: the formula behind every warning and error (ADR 0013).

A sheet is a list of cells: inputs, each with its value, unit and source, and formulas over the
cells above them; then the requirements a design must meet. The engine evaluates the sheet to raise
its findings, and the web page evaluates the same formulas when the builder edits an input, so the
formula language is small and has a twin in ``web/src/sheet.ts``. ``core/tests/expressions.json``
holds the two to the same answers.

The language: numbers, names, ``+ - * / ^``, brackets, and the functions in ``ARITY``. ``^`` binds
tighter than a leading minus (``-x^2`` is ``-(x^2)``) and groups to the right. Everything is in SI.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import cache
from typing import Literal

import pint
from pydantic import BaseModel, ConfigDict

from kilndesigner.units import Q_, Quantity

Level = Literal["warning", "error"]
Status = Literal["pass", "warning", "error"]
Op = Literal["<=", "<", ">=", ">"]

ARITY: dict[str, int] = {
    "sqrt": 1, "exp": 1, "ln": 1, "log10": 1, "abs": 1,
    "sin": 1, "cos": 1, "tan": 1, "asin": 1, "acos": 1, "atan": 1, "atan2": 2,
    "min": -2, "max": -2,
}  # fmt: skip
"""Each function's number of arguments; -2 means two or more."""
CONSTANTS = {"pi": math.pi, "π": math.pi}


class ExpressionError(ValueError):
    """A formula that can't be read, names a cell that isn't above it, or has the wrong units."""


# ---- Reading a formula ----------------------------------------------------------------------


@dataclass(frozen=True)
class Num:
    value: float
    text: str


@dataclass(frozen=True)
class Name:
    id: str


@dataclass(frozen=True)
class Neg:
    arg: Node


@dataclass(frozen=True)
class Bin:
    op: Literal["+", "-", "*", "/", "^"]
    left: Node
    right: Node


@dataclass(frozen=True)
class Call:
    fn: str
    args: tuple[Node, ...]


type Node = Num | Name | Neg | Bin | Call

_TOKEN = re.compile(
    r"\s*(?:(?P<num>(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)|(?P<name>[^\W\d]\w*)|(?P<op>[-+*/^(),]))"
)
NAME = re.compile(r"^[^\W\d]\w*$")


def _tokens(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    pos, end = 0, len(text.rstrip())
    while pos < end:
        m = _TOKEN.match(text, pos)
        if m is None or m.lastgroup is None:
            raise ExpressionError(f"can't read {text[pos:].strip()!r} in {text!r}")
        out.append((m.lastgroup, m.group(m.lastgroup)))
        pos = m.end()
    return out


class _Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.toks = _tokens(text)
        self.i = 0

    def peek(self) -> str | None:
        return self.toks[self.i][1] if self.i < len(self.toks) else None

    def take(self) -> tuple[str, str]:
        if self.i >= len(self.toks):
            raise ExpressionError(f"{self.text!r} ends too soon")
        self.i += 1
        return self.toks[self.i - 1]

    def expect(self, tok: str) -> None:
        kind, got = self.take()
        if kind != "op" or got != tok:
            raise ExpressionError(f"expected {tok!r} but found {got!r} in {self.text!r}")

    def parse(self) -> Node:
        node = self.sum()
        if self.i < len(self.toks):
            raise ExpressionError(f"unexpected {self.toks[self.i][1]!r} in {self.text!r}")
        return node

    def sum(self) -> Node:
        node = self.term()
        while (op := self.peek()) in ("+", "-"):
            self.take()
            node = Bin("+" if op == "+" else "-", node, self.term())
        return node

    def term(self) -> Node:
        node = self.unary()
        while (op := self.peek()) in ("*", "/"):
            self.take()
            node = Bin("*" if op == "*" else "/", node, self.unary())
        return node

    def unary(self) -> Node:
        if self.peek() == "-" and self.toks[self.i][0] == "op":
            self.take()
            return Neg(self.unary())
        return self.power()

    def power(self) -> Node:
        base = self.atom()
        if self.peek() == "^":
            self.take()
            return Bin("^", base, self.unary())
        return base

    def atom(self) -> Node:
        kind, tok = self.take()
        if kind == "num":
            return Num(float(tok), tok)
        if kind == "name":
            if self.peek() != "(":
                if tok in ARITY:
                    raise ExpressionError(f"{tok} needs brackets in {self.text!r}")
                return Name(tok)
            if tok not in ARITY:
                raise ExpressionError(f"{tok!r} is not a function the sheets know")
            self.take()
            args = [self.sum()]
            while self.peek() == ",":
                self.take()
                args.append(self.sum())
            self.expect(")")
            n = ARITY[tok]
            if (n > 0 and len(args) != n) or (n < 0 and len(args) < -n):
                raise ExpressionError(f"{tok} takes {n if n > 0 else 'two or more'} arguments")
            return Call(tok, tuple(args))
        if tok == "(":
            node = self.sum()
            self.expect(")")
            return node
        raise ExpressionError(f"unexpected {tok!r} in {self.text!r}")


@cache
def parse(text: str) -> Node:
    """Read a formula into its tree."""
    return _Parser(text).parse()


def names(node: Node) -> set[str]:
    """The cells a formula reads."""
    match node:
        case Num():
            return set()
        case Name(id=n):
            return set() if n in CONSTANTS else {n}
        case Neg(arg=a):
            return names(a)
        case Bin(left=a, right=b):
            return names(a) | names(b)
        case Call(args=args):
            return set().union(*(names(a) for a in args))


# ---- Evaluating ------------------------------------------------------------------------------
# IEEE arithmetic, as the page's JavaScript does it: a domain error is NaN, an overflow infinity.


def _div(a: float, b: float) -> float:
    if b != 0:
        return a / b
    if a == 0 or math.isnan(a):
        return math.nan
    return math.copysign(math.inf, a) * math.copysign(1, b)


def _pow(a: float, b: float) -> float:
    try:
        return math.pow(a, b)
    except OverflowError:
        return math.inf
    except ValueError:
        return math.inf if a == 0 and b < 0 else math.nan


def _guard(f: Callable[..., float]) -> Callable[..., float]:
    def g(*xs: float) -> float:
        try:
            return float(f(*xs))
        except OverflowError:
            return math.inf
        except ValueError:
            return math.nan

    return g


def _log(f: Callable[[float], float]) -> Callable[[float], float]:
    return lambda x: -math.inf if x == 0 else _guard(f)(x)


def _extreme(pick: Callable[..., float]) -> Callable[..., float]:
    return lambda *xs: math.nan if any(math.isnan(x) for x in xs) else pick(xs)


_FUNCS: dict[str, Callable[..., float]] = {
    "sqrt": _guard(math.sqrt), "exp": _guard(math.exp), "ln": _log(math.log),
    "log10": _log(math.log10), "abs": abs, "sin": _guard(math.sin), "cos": _guard(math.cos),
    "tan": _guard(math.tan), "asin": _guard(math.asin), "acos": _guard(math.acos),
    "atan": math.atan, "atan2": math.atan2, "min": _extreme(min), "max": _extreme(max),
}  # fmt: skip


def evaluate(node: Node, env: Mapping[str, float]) -> float:
    """A formula's value, in SI, from the cells' SI values."""
    match node:
        case Num(value=v):
            return v
        case Name(id=n):
            if n in CONSTANTS:
                return CONSTANTS[n]
            if n not in env:
                raise ExpressionError(f"{n!r} is not a cell above this one")
            return env[n]
        case Neg(arg=a):
            return -evaluate(a, env)
        case Bin(op=op, left=a, right=b):
            x, y = evaluate(a, env), evaluate(b, env)
            if op == "+":
                return x + y
            if op == "-":
                return x - y
            if op == "*":
                return x * y
            return _div(x, y) if op == "/" else _pow(x, y)
        case Call(fn=fn, args=args):
            return _FUNCS[fn](*(evaluate(a, env) for a in args))


def _plain(q: Quantity, where: str) -> float:
    try:
        return float(q.to("dimensionless").magnitude)
    except pint.DimensionalityError as e:
        raise ExpressionError(f"{where} needs a number with no unit, not {q.units}") from e


def dimensions(node: Node, env: Mapping[str, Quantity]) -> Quantity:
    """A formula evaluated with Pint quantities, to check its units."""
    match node:
        case Num(value=v):
            return Q_(v)
        case Name(id=n):
            return Q_(CONSTANTS[n]) if n in CONSTANTS else env[n]
        case Neg(arg=a):
            return -dimensions(a, env)
        case Bin(op="^", left=a, right=b):
            return dimensions(a, env) ** _plain(dimensions(b, env), "a power")
        case Bin(op=op, left=a, right=b):
            x, y = dimensions(a, env), dimensions(b, env)
            try:
                if op == "+":
                    return x + y
                if op == "-":
                    return x - y
            except pint.DimensionalityError as e:
                raise ExpressionError(f"can't {'add' if op == '+' else 'subtract'} {y.units} "
                                      f"and {x.units}") from e  # fmt: skip
            return x * y if op == "*" else x / y
        case Call(fn="sqrt", args=(a,)):
            return dimensions(a, env) ** 0.5
        case Call(fn="abs", args=(a,)):
            return abs(dimensions(a, env))
        case Call(fn="min" | "max" | "atan2" as fn, args=args):
            qs = [dimensions(a, env) for a in args]
            try:
                if fn == "atan2":  # the angle of a rise over a run: any one unit for both
                    y, x = qs
                    return Q_(math.atan2(y.magnitude, x.to(y.units).magnitude))
                return min(qs) if fn == "min" else max(qs)
            except pint.DimensionalityError as e:
                raise ExpressionError(f"{fn} of values in different units") from e
        case Call(fn=fn, args=args):
            return Q_(_FUNCS[fn](*(_plain(dimensions(a, env), fn) for a in args)))


# ---- Writing a formula out -------------------------------------------------------------------

_PREC = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 4}
_SUPER = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _prec(node: Node) -> int:
    match node:
        case Bin(op=op):
            return _PREC[op]
        case Neg():
            return 3
        case _:
            return 5


def shown(node: Node) -> str:
    """A formula as a builder reads it: ``π/4·d²``, ``√(a² + b²)``, ``P − Q``."""

    def wrap(n: Node, ok: bool) -> str:
        return shown(n) if ok else f"({shown(n)})"

    match node:
        case Num(text=t):
            return t
        case Name(id=n):
            return "π" if n == "pi" else n
        case Neg(arg=a):
            return "−" + wrap(a, _prec(a) > 3)
        case Bin(op="^", left=a, right=b):
            base = wrap(a, _prec(a) == 5)
            if isinstance(b, Num) and b.text.isdigit():
                return base + b.text.translate(_SUPER)
            return f"{base}^{wrap(b, _prec(b) == 5)}"
        case Bin(op=op, left=a, right=b):
            p = _PREC[op]
            left = wrap(a, _prec(a) >= p)
            right = wrap(b, _prec(b) > p or (op in "+*" and _prec(b) == p))
            return {"+": f"{left} + {right}", "-": f"{left} − {right}", "*": f"{left}·{right}",
                    "/": f"{left}/{right}"}[op]  # fmt: skip
        case Call(fn="sqrt", args=(a,)):
            return "√" + wrap(a, _prec(a) == 5)
        case Call(fn="abs", args=(a,)):
            return f"|{shown(a)}|"
        case Call(fn=fn, args=args):
            return f"{fn}({', '.join(shown(a) for a in args)})"


_EXCEL = {"ln": "LN", "log10": "LOG10", "atan2": "ATAN2"}


def excel(node: Node, ref: Mapping[str, str]) -> str:
    """A formula in spreadsheet syntax, each name replaced by its cell (``ref``); fully bracketed,
    because a spreadsheet's leading minus binds tighter than its ``^``."""
    match node:
        case Num(text=t):
            return t
        case Name(id=n):
            return "PI()" if n in CONSTANTS else ref[n]
        case Neg(arg=a):
            return f"(-{excel(a, ref)})"
        case Bin(op=op, left=a, right=b):
            return f"({excel(a, ref)}{op}{excel(b, ref)})"
        case Call(fn="atan2", args=(y, x)):  # ATAN2 takes x first
            return f"ATAN2({excel(x, ref)},{excel(y, ref)})"
        case Call(fn=fn, args=args):
            return f"{_EXCEL.get(fn, fn.upper())}({','.join(excel(a, ref) for a in args)})"


# ---- Numbers as the sheets print them ---------------------------------------------------------


def _round(x: float, places: int) -> float:
    """Half away from zero, as the page rounds; ``places`` ≥ 0."""
    f = float(10**places)
    return math.copysign(math.floor(abs(x) * f + 0.5) / f, x)


def _scaled(x: float, e: int) -> float:
    """x ÷ 10^e using only exact powers of ten, so JavaScript gets the same bits."""
    return x / float(10**e) if e >= 0 else x * float(10**-e)


def number(x: float) -> str:
    """Four significant figures, thousands separated; powers of ten outside 0.001 to 1,000,000.
    ``web/src/sheet.ts`` prints the same text."""
    if math.isnan(x):
        return "—"
    if math.isinf(x):
        return "∞" if x > 0 else "−∞"
    a = abs(x)
    if a == 0:
        return "0"
    e = math.floor(math.log10(a))
    if abs(_scaled(a, e)) >= 10:  # log10 an ulp off either side of a power of ten
        e += 1
    elif abs(_scaled(a, e)) < 1:
        e -= 1
    if a >= 1e6 or a < 1e-3:
        m = _round(_scaled(x, e), 3)
        if abs(m) >= 10:
            m, e = m / 10, e + 1
        text = f"{m:.3f}".rstrip("0").rstrip(".")
        return f"{text.replace('-', '−')} × 10{str(e).translate(_SUPER)}"
    places = max(0, 3 - e)
    text = f"{_round(x, places):,.{places}f}"
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text.replace("-", "−")


# ---- The sheet -------------------------------------------------------------------------------


class Cell(BaseModel):
    """One row: an input (no ``expr``) or a formula over the rows above. A fact that isn't a number
    has ``text`` and no ``value``."""

    model_config = ConfigDict(frozen=True)

    symbol: str
    meaning: str
    value: float | None = None
    """In SI."""
    text: str | None = None
    unit: str = ""
    """The unit it is shown in, as Pint writes it; empty for a plain number."""
    label: str = ""
    """The unit as printed: ``in²``, ``°F``."""
    scale: float = 1.0
    offset: float = 0.0
    """Shown value = SI value × scale + offset."""
    expr: str | None = None
    formula: str | None = None
    """``expr`` as printed."""
    source: str | None = None


class Requirement(BaseModel):
    model_config = ConfigDict(frozen=True)

    left: str
    op: Op
    right: str
    level: Level
    holds: bool
    margin: str
    """How close: ``σ = 1,577 psi, 13.14 % of σ_allow = 12,000 psi``."""


class Lever(BaseModel):
    """The input the builder controls, and the range (SI) to look for a change of state in."""

    model_config = ConfigDict(frozen=True)

    symbol: str
    lo: float
    hi: float
    step: float | None = None
    """For a lever that comes in whole steps (cylinders, burners): the answer is rounded to the
    next step that passes."""


class Check(BaseModel):
    """Why a finding was raised: its sheet, the requirements, and what would change the result."""

    model_config = ConfigDict(frozen=True)

    id: str
    title: str
    label: str | None = None
    """Its finding's mark in the report, the plans and the workbook: E1, W2."""
    reference: str | None = None
    cells: list[Cell]
    requirements: list[Requirement]
    rule: str | None = None
    """For a check that isn't a formula: the rule, stated."""
    rule_holds: bool = True
    rule_level: Level = "error"
    lever: Lever | None = None
    status: Status
    solve: str | None = None
    """``Passes when d ≥ 0.5203 in``."""


_RANK: dict[Status, int] = {"pass": 0, "warning": 1, "error": 2}


def _slack(a: float, b: float) -> float:
    """≤ and ≥ allow a part in a billion: a value on its limit passes whichever way the floating
    point fell. ``web/src/sheet.ts`` allows the same."""
    return 1e-9 * max(abs(a), abs(b)) if math.isfinite(a) and math.isfinite(b) else 0.0


_OPS: dict[Op, Callable[[float, float], bool]] = {
    "<=": lambda a, b: a <= b + _slack(a, b), "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b - _slack(a, b), ">": lambda a, b: a > b,
}  # fmt: skip
_SHOWN_OP = {"<=": "≤", "<": "<", ">=": "≥", ">": ">"}


def _show(c: Cell, v: float) -> str:
    text = number(v * c.scale + c.offset)
    return f"${text}" if c.label == "$" else f"{text} {c.label}".rstrip()


def values(cells: list[Cell], given: Mapping[str, float] | None = None) -> dict[str, float]:
    """Every numeric cell's SI value, with ``given`` replacing inputs."""
    env: dict[str, float] = {}
    for c in cells:
        if c.expr is not None:
            env[c.symbol] = evaluate(parse(c.expr), env)
        elif c.value is not None:
            env[c.symbol] = (given or {}).get(c.symbol, c.value)
    return env


def _margin(left: Cell, op: Op, right: Cell, a: float, b: float) -> str:
    lt, rt = f"{left.symbol} = {_show(left, a)}", f"{right.symbol} = {_show(right, b)}"
    if left.offset or right.offset:  # a ratio of temperatures means nothing: give the difference
        d = (a - b) * left.scale
        return f"{lt}, {number(abs(d))} {left.label} {'over' if d > 0 else 'under'} {rt}"
    if b != 0 and math.isfinite(a) and math.isfinite(b) and a / b > 0:
        return f"{lt}, {number(100 * a / b)} % of {rt}"
    return f"{lt} against {rt}"


def _status(check: Check, env: Mapping[str, float]) -> Status:
    worst: Status = "pass" if check.rule_holds else check.rule_level
    for r in check.requirements:
        if not _OPS[r.op](env[r.left], env[r.right]) and _RANK[r.level] > _RANK[worst]:
            worst = r.level
    return worst


STEPS = 64
"""How finely :func:`solve` walks out from the lever's value before it bisects: fine enough to
find a passing stretch with failures either side (too few cylinders, or more than the regulator
passes)."""


def solve(check: Check) -> str | None:
    """Where the lever nearest changes the result: walk out from its value towards each end of its
    range, then bisect at the first step that differs. ``web/src/sheet.ts`` does the same, live."""
    if check.lever is None:
        return None
    lv = check.lever
    cell = next(c for c in check.cells if c.symbol == lv.symbol)
    assert cell.value is not None

    def passes(x: float) -> bool:
        return _status(check, values(check.cells, {lv.symbol: x})) == "pass"

    x0 = cell.value
    p0 = passes(x0)
    found: list[float] = []
    for end in (lv.lo, lv.hi):
        prev = x0
        for k in range(1, STEPS + 1) if end != x0 else ():
            x = x0 + (end - x0) * k / STEPS
            if passes(x) != p0:
                a, b = prev, x
                for _ in range(60):
                    m = (a + b) / 2
                    a, b = (m, b) if passes(m) == p0 else (a, m)
                found.append(a if p0 else b)
                break
            prev = x
    sym = lv.symbol
    if not found:
        span = f"{sym} from {_show(cell, lv.lo)} to {_show(cell, lv.hi)}"
        return f"Passes for any {span}" if p0 else f"Doesn't pass for any {span}"
    x = min(found, key=lambda v: abs(v - x0))
    up = (x > x0) != p0  # failing: passes above x if x is above; passing: holds while below
    if abs(x * cell.scale + cell.offset) < 1e-6 * abs(lv.hi - lv.lo) * cell.scale:
        x = -cell.offset / cell.scale  # a limit of 0 °F, not the slack's −4.6 × 10⁻⁷ °F
    if lv.step:  # 5 cylinders, not 4.331: the next whole step on the side that passes
        n = x / lv.step
        whole = lv.step * (math.ceil(n - 1e-9) if up else math.floor(n + 1e-9))
        if not passes(whole):
            return (
                f"No whole {sym} passes (it would at {sym} {'≥' if up else '≤'} {_show(cell, x)})"
            )
        x = whole
    return f"{'Passes while' if p0 else 'Passes when'} {sym} {'≥' if up else '≤'} {_show(cell, x)}"


def _scale(si_unit: str, unit: str) -> tuple[float, float]:
    zero = float(Q_(0.0, si_unit).to(unit).magnitude)
    return float(Q_(1.0, si_unit).to(unit).magnitude) - zero, zero


class Sheet:
    """Build a check row by row, then :meth:`check` it::

    s = Sheet("frame.rod", "Tie rod stress, hot", reference=ROD_SOURCE)
    s.given("P", "load on each rod, hot", Q_(224, "lbf"), source="working: Tie rod load")
    s.given("d", "rod root diameter", Q_(0.4001, "in"), source="ASME B1.1")
    s.let("A", "root area", "pi/4*d^2", "in**2")
    s.let("σ", "stress", "P/A", "psi")
    s.given("σ_allow", "allowable stress", Q_(12000, "psi"), source=AISC)
    s.require("σ", "<=", "σ_allow")
    s.lever("d", Q_(0.1, "in"), Q_(2, "in"))
    check = s.check()
    """

    def __init__(self, id: str, title: str, reference: str | None = None) -> None:
        self.id, self.title, self.reference = id, title, reference
        self.cells: list[Cell] = []
        self.env: dict[str, float] = {}
        self.dims: dict[str, Quantity] = {}
        self.reqs: list[tuple[str, Op, str, Level]] = []
        self._lever: Lever | None = None
        self._rule: tuple[str, bool, Level] | None = None

    def _name(self, symbol: str) -> None:
        if not NAME.match(symbol) or symbol in ARITY or symbol in CONSTANTS:
            raise ExpressionError(f"{symbol!r} can't name a cell")
        if symbol in self.env:
            raise ExpressionError(f"{symbol!r} is already a cell in {self.id}")

    def given(
        self,
        symbol: str,
        meaning: str,
        value: Quantity | float,
        unit: str | None = None,
        source: str | None = None,
    ) -> float:
        """An input: its value (a quantity, or a plain number), shown in ``unit`` (default: the
        quantity's own). Returns its SI value."""
        self._name(symbol)
        q = value if isinstance(value, pint.Quantity) else Q_(float(value))
        base = q.to_base_units()
        si_unit = str(base.units)
        shown_in = unit if unit is not None else ("" if q.unitless else str(q.units))
        scale, offset = _scale(si_unit, shown_in or "dimensionless")
        self.env[symbol] = float(base.magnitude)
        self.dims[symbol] = Q_(float(base.magnitude), si_unit)
        self.cells.append(
            Cell(
                symbol=symbol, meaning=meaning, value=float(base.magnitude), unit=shown_in,
                label=_label(shown_in), scale=scale, offset=offset, source=source,
            )
        )  # fmt: skip
        return self.env[symbol]

    def fact(self, meaning: str, text: str, source: str | None = None) -> None:
        """Something the check was applied to that isn't a number: a material, a choice."""
        self.cells.append(Cell(symbol="", meaning=meaning, text=text, source=source))

    def let(
        self, symbol: str, meaning: str, expr: str, unit: str = "", source: str | None = None
    ) -> float:
        """A formula over the cells above, shown in ``unit``. Returns its SI value."""
        self._name(symbol)
        node = parse(expr)
        missing = names(node) - self.env.keys()
        if missing:
            raise ExpressionError(f"{symbol} = {expr} reads {sorted(missing)}, not cells above it")
        si_unit = str(Q_(1.0, unit or "dimensionless").to_base_units().units)
        got = dimensions(node, self.dims)
        try:
            got.to(si_unit)
        except pint.DimensionalityError as e:
            raise ExpressionError(
                f"{symbol} = {expr} comes out in {got.to_base_units().units}, "
                f"not {unit or 'a plain number'}"
            ) from e
        value = evaluate(node, self.env)
        self.env[symbol] = value
        self.dims[symbol] = Q_(value, si_unit)
        scale, offset = _scale(si_unit, unit or "dimensionless")
        self.cells.append(
            Cell(
                symbol=symbol, meaning=meaning, value=value, unit=unit, label=_label(unit),
                scale=scale, offset=offset, expr=expr, formula=shown(node), source=source,
            )
        )  # fmt: skip
        return value

    def require(self, left: str, op: Op, right: str, level: Level = "error") -> bool:
        """``left op right`` must hold, or the check raises ``level``. Returns whether it holds."""
        for s in (left, right):
            if s not in self.env:
                raise ExpressionError(f"{s!r} is not a cell in {self.id}")
        try:
            self.dims[left].to(self.dims[right].units)
        except pint.DimensionalityError as e:
            raise ExpressionError(f"can't compare {left} with {right}: different units") from e
        self.reqs.append((left, op, right, level))
        return _OPS[op](self.env[left], self.env[right])

    def rule(self, statement: str, holds: bool, level: Level = "error") -> None:
        """A requirement that isn't a formula, stated, and whether the design meets it."""
        self._rule = (statement, holds, level)

    def lever(
        self, symbol: str, lo: Quantity | float, hi: Quantity | float, step: float | None = None
    ) -> None:
        """The input the builder controls, and the range to solve over; ``step`` (SI) for one that
        comes in whole steps, such as a count."""
        if symbol not in self.env or any(c.symbol == symbol and c.expr for c in self.cells):
            raise ExpressionError(f"the lever {symbol!r} must be an input of {self.id}")

        def si(v: Quantity | float) -> float:
            return float(v.to_base_units().magnitude) if isinstance(v, pint.Quantity) else v

        self._lever = Lever(symbol=symbol, lo=si(lo), hi=si(hi), step=step)

    def agrees(self, symbol: str, value: Quantity | float, rel: float = 1e-6) -> None:
        """The engine's own result for a cell: the sheet must give the same, or it isn't the
        calculation it claims to be."""
        want = float(value.to_base_units().magnitude) if isinstance(value, pint.Quantity) else value
        got = self.env[symbol]
        if not math.isclose(got, want, rel_tol=rel, abs_tol=1e-12):
            raise SheetMismatchError(
                f"{self.id}: the sheet gives {symbol} = {got}, the engine {want}"
            )

    def check(self) -> Check:
        by = {c.symbol: c for c in self.cells}
        reqs = [
            Requirement(
                left=a, op=op, right=b, level=level,
                holds=_OPS[op](self.env[a], self.env[b]),
                margin=_margin(by[a], op, by[b], self.env[a], self.env[b]),
            )
            for a, op, b, level in self.reqs
        ]  # fmt: skip
        statement, holds, level = self._rule or (None, True, "error")
        draft = Check(
            id=self.id, title=self.title, reference=self.reference, cells=self.cells,
            requirements=reqs, rule=statement, rule_holds=holds, rule_level=level,
            lever=self._lever, status="pass",
        )  # fmt: skip
        return draft.model_copy(update={"status": _status(draft, self.env), "solve": solve(draft)})


class SheetMismatchError(AssertionError):
    """A sheet that doesn't reproduce the engine's own number: a bug in one or the other."""


def _label(unit: str) -> str:
    label = f"{Q_(1.0, unit).units:~P}" if unit else ""
    return "°" if label == "deg" else label


def requirement_text(r: Requirement) -> str:
    return f"{r.left} {_SHOWN_OP[r.op]} {r.right}"


def cell_text(c: Cell) -> str:
    """A cell's value as the sheet shows it, ``1,782 psi``, or its fact."""
    return c.text or "" if c.value is None else _show(c, c.value)


__all__ = [
    "Cell",
    "Check",
    "ExpressionError",
    "Lever",
    "Requirement",
    "Sheet",
    "SheetMismatchError",
    "cell_text",
    "dimensions",
    "evaluate",
    "excel",
    "number",
    "parse",
    "requirement_text",
    "shown",
    "solve",
    "values",
]
