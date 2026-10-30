"""What every validation notebook shares: one engine figure against one published figure.

Each notebook builds a list of ``compare(...)`` rows named ``results``; the test
``core/tests/test_validation_notebooks.py`` runs every notebook and fails if a row is out of its
tolerance (ADR 0009).
"""

from __future__ import annotations

from typing import Any


def compare(
    case: str,
    source: str,
    engine: float,
    published: float,
    tolerance: float,
    *,
    absolute: bool = False,
    ceiling: bool = False,
) -> dict[str, Any]:
    """One engine figure against a published one; ``tolerance`` is relative unless ``absolute``.
    With ``ceiling`` the published figure is a most: the engine may be any amount under it."""
    error = engine - published if absolute else engine / published - 1
    return {
        "case": case,
        "source": source,
        "engine": engine,
        "published": published,
        "error": error,
        "tolerance": tolerance,
        "absolute": absolute,
        "ceiling": ceiling,
        "ok": error <= tolerance if ceiling else abs(error) <= tolerance,
    }


def markdown(rows: list[dict[str, Any]]) -> str:
    """The rows as a Markdown table."""
    lines = [
        "| case | source | engine | published | error | tolerance | within |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if r["absolute"]:
            err, tol = f"{r['error']:+.3g}", f"±{r['tolerance']:g}"
        else:
            err, tol = f"{100 * r['error']:+.2f} %", f"±{100 * r['tolerance']:g} %"
        if r["ceiling"]:
            tol = f"at most {tol.lstrip('±')} over"
        lines.append(
            f"| {r['case']} | {r['source']} | {r['engine']:.6g} | {r['published']:.6g} | {err} | "
            f"{tol} | {'yes' if r['ok'] else '**NO**'} |"
        )
    return "\n".join(lines)
