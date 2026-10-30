"""The checks as a workbook: one worksheet per check, with live formulas (ADR 0013).

Each worksheet lists the check's cells. An input's value is typed in its own unit (column C) and
turned into SI beside it (column G); a formula works on the SI column and is shown back in its
unit. Change an input and everything below it recomputes, as in the web page. Each formula cell
also stores the engine's result, so the file reads correctly before a spreadsheet recalculates.
"""

from __future__ import annotations

import io
import re

import xlsxwriter
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from kilndesigner.sheet import Cell, Check, excel, parse, requirement_text

HEADER = ["Symbol", "Meaning", "Value", "Unit", "Formula", "Source", "SI value"]
FIRST = 5  # the row (0-based) of the first cell: below the title, status, reference and header
WIDTHS = [10, 34, 14, 10, 26, 50, 16]


def _sheet_name(label: str, title: str, taken: set[str]) -> str:
    base = re.sub(r"[\[\]:*?/\\']", "", f"{label} {title}")[:31].rstrip()
    name, n = base, 2
    while name.lower() in taken:
        name = f"{base[:28]}~{n}"
        n += 1
    taken.add(name.lower())
    return name


def _number(x: float) -> str:
    return repr(float(x))


def _to_si(c: Cell, ref: str) -> str:
    """Column G for an input: its shown value back in SI."""
    shifted = f"({ref}-{_number(c.offset)})" if c.offset else ref
    return f"={shifted}/{_number(c.scale)}" if c.scale != 1 else f"={shifted}"


def _to_shown(c: Cell, ref: str) -> str:
    scaled = f"{ref}*{_number(c.scale)}" if c.scale != 1 else ref
    return f"={scaled}+{_number(c.offset)}" if c.offset else f"={scaled}"


def _holds(op: str, a: str, b: str) -> str:
    """A requirement as a formula, with the part in a billion that ≤ and ≥ allow in the engine
    and the page (kilndesigner.sheet._slack), so a value on its limit passes here too."""
    if op not in ("<=", ">="):
        return f"={a}{op}{b}"
    slack = f"1E-9*MAX(ABS({a}),ABS({b}))"
    return f"={a}<={b}+{slack}" if op == "<=" else f"={a}>={b}-{slack}"


def _formula(
    ws: Worksheet, row: int, col: int, formula: str, fmt: Format | None, value: object
) -> None:
    """A formula and the engine's value for it, which a spreadsheet shows until it recalculates."""
    ws.write_formula(row, col, formula, fmt, value)  # pyright: ignore[reportArgumentType]


def checks_workbook(checks: list[Check]) -> bytes:
    """The workbook of ``checks``, as the bytes of an .xlsx file."""
    out = io.BytesIO()
    book = xlsxwriter.Workbook(out, {"in_memory": True})
    bold = book.add_format({"bold": True})
    title = book.add_format({"bold": True, "font_size": 14})
    head = book.add_format({"bold": True, "bottom": 1, "bg_color": "#EEEEEE"})
    given = book.add_format({"bg_color": "#FFF7D6", "border": 1, "border_color": "#C9B458"})
    muted = book.add_format({"font_color": "#666666"})
    wrap = book.add_format({"text_wrap": True, "valign": "top"})
    percent = book.add_format({"num_format": "0.0%"})
    index = book.add_worksheet("Checks")
    index.write_row(0, 0, ["Mark", "Check", "Result", "Worksheet"], head)
    index.set_column(0, 0, 8)
    index.set_column(1, 1, 50)
    index.set_column(2, 3, 16)
    taken = {"checks"}
    for i, check in enumerate(checks):
        label = check.label or f"C{i + 1}"
        name = _sheet_name(label, check.title, taken)
        ws = book.add_worksheet(name)
        _write_check(ws, check, label, (bold, title, head, given, muted, wrap, percent))
        index.write_string(i + 1, 0, label)
        index.write_string(i + 1, 1, check.title)
        index.write_string(i + 1, 2, check.status)
        index.write_url(i + 1, 3, f"internal:'{name}'!A1", string="Open")
    book.close()
    return out.getvalue()


def _write_check(ws: Worksheet, check: Check, label: str, formats: tuple[Format, ...]) -> None:
    bold, title, head, given, muted, wrap, percent = formats
    for col, width in enumerate(WIDTHS):
        ws.set_column(col, col, width, wrap if col in (1, 5) else None)
    ws.write_string(0, 0, f"{label} · {check.title}", title)
    if check.reference:
        ws.write_string(2, 0, f"Source: {check.reference}", muted)
    ws.write_row(FIRST - 1, 0, HEADER, head)
    ref: dict[str, str] = {}
    row = FIRST
    for c in check.cells:
        r1 = row + 1  # the spreadsheet's own 1-based row number
        ws.write_string(row, 0, c.symbol)
        ws.write_string(row, 1, c.meaning)
        ws.write_string(row, 3, c.label)
        if c.formula:
            ws.write_string(row, 4, f"{c.symbol} = {c.formula}")
        if c.source:
            ws.write_string(row, 5, c.source)
        if c.value is None:  # a fact, not a number
            ws.write_string(row, 2, c.text or "")
            row += 1
            continue
        shown = c.value * c.scale + c.offset
        if c.expr is None:
            ws.write_number(row, 2, shown, given)
            _formula(ws, row, 6, _to_si(c, f"C{r1}"), muted, c.value)
        else:
            _formula(ws, row, 6, "=" + excel(parse(c.expr), ref), muted, c.value)
            _formula(ws, row, 2, _to_shown(c, f"G{r1}"), None, shown)
        ref[c.symbol] = f"G{r1}"
        row += 1
    row += 1
    by = {c.symbol: c for c in check.cells}
    holds: dict[str, list[str]] = {"error": [], "warning": []}
    if check.requirements:
        ws.write_row(row, 0, ["Requirement", "Holds", "Ratio", "If not"], head)
        row += 1
        for q in check.requirements:
            a, b = ref[q.left], ref[q.right]
            ws.write_string(row, 0, requirement_text(q))
            _formula(ws, row, 1, _holds(q.op, a, b), None, q.holds)
            left, right = by[q.left], by[q.right]
            if not (left.offset or right.offset):  # a ratio of temperatures means nothing
                ratio = (left.value or 0) / right.value if right.value else 0
                _formula(ws, row, 2, f'=IF({b}=0,"",{a}/{b})', percent, ratio)
            ws.write_string(row, 3, q.level)
            holds[q.level].append(f"B{row + 1}")
            row += 1
    if check.rule:
        ws.write_string(row, 0, "Rule", bold)
        ws.write_string(row, 1, check.rule)
        ws.write_string(row, 2, "holds" if check.rule_holds else f"fails: {check.rule_level}")
        row += 1
    row += 1
    ws.write_string(row, 0, "Result", bold)
    errors = "TRUE" if not holds["error"] else f"AND({','.join(holds['error'])})"
    warnings = "TRUE" if not holds["warning"] else f"AND({','.join(holds['warning'])})"
    if not check.rule_holds:
        errors = "FALSE" if check.rule_level == "error" else errors
        warnings = "FALSE" if check.rule_level == "warning" else warnings
    _formula(
        ws, row, 1, f'=IF({errors},IF({warnings},"pass","warning"),"error")', bold, check.status
    )
    if check.solve:
        lever = f" (try Goal Seek on {check.lever.symbol}'s value)" if check.lever else ""
        ws.write_string(row + 1, 0, "Engine", bold)
        ws.write_string(row + 1, 1, f"{check.solve} at the values above{lever}.")


__all__ = ["checks_workbook"]
