"""The reference kilns' printed facts (``reference_kilns.yaml``), read for engine v2's validation
(ADR 0017).

Each fact carries its Olsen page and a status (printed, derived, scaled, drawing, assumed); see
the file's header. Heat facts that describe one firing share a ``firing`` label, so a time is
compared only with the fuel or burners of the same firing; unlabelled facts form one firing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pint
import yaml

from kilndesigner.units import Q_, si, ureg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = HERE / "reference_kilns.yaml"

type Fact = dict[str, Any]

STATUSES = frozenset({"printed", "derived", "scaled", "drawing", "assumed"})
BOUNDS = frozenset({"=", "<", "<=", ">", ">=", "~"})
READINGS = frozenset({"flagged", "uncertain"})
COUNT_UNITS = frozenset(
    {"bundle", "shovel", "piece", "brick", "stoking", "firing", "burner", "chamber", "shelf"}
)
HEAT = frozenset((
    "cone", "top_temperature", "firing_time", "stage_time", "preheat_time", "cooling_time",
    "hold_time", "fuel_per_firing", "fuel_rate", "energy_per_firing", "fuel_kind", "burner_count",
    "burner_type", "burner_model", "burner_rating", "burner_input", "input_per_volume", "gas",
    "gas_pressure", "orifice", "oil_rate", "nozzle", "element_power", "voltage", "current",
    "surface_load", "atmosphere", "schedule", "damper_schedule", "ware", "setting", "evenness",
    "altitude", "wall_heat_loss", "wall_heat_storage", "cold_face_temperature",
))  # fmt: skip
CHAMBER = frozenset((
    "volume", "stacking_volume", "width", "depth", "height", "springline_height", "crown_height",
    "length", "diameter", "chamber_count", "slope", "floor_area", "shape",
))  # fmt: skip
LINING = frozenset((
    "wall", "wall_thickness", "roof", "roof_thickness", "floor", "floor_thickness", "door",
    "insulation", "backing", "mortar",
))  # fmt: skip
FLOW = frozenset((
    "firebox_count", "firebox", "firebox_width", "firebox_length", "firebox_height", "grate",
    "grate_area", "ash_pit", "inlet_flue", "exit_flue", "exit_flue_area", "between_flues",
    "chimney_count", "chimney_height", "chimney_section", "chimney_run", "damper", "burner_port",
    "stoke_hole", "spy_hole", "passive_air", "bag_wall", "salt_port",
))  # fmt: skip
STRUCTURE = frozenset((
    "roof_type", "span", "rise", "rise_per_ft", "ring_thickness", "arch_material", "skewback",
    "springline_height", "wall_height", "buttress", "frame", "tie_rods", "bands", "dome_type",
    "dome_diameter", "dome_rise", "dome_thickness", "vault_length", "foundation", "earth_backing",
    "door_arch", "floor_structure", "expansion_joint", "construction", "failure",
))  # fmt: skip
SERVICE = frozenset((
    "builder", "built", "build_time", "firings", "service_life", "use", "rebuilt", "condition",
))  # fmt: skip
VOCAB: dict[str, frozenset[str]] = {
    "heat": HEAT,
    "chamber": CHAMBER,
    "lining": LINING,
    "flow": FLOW,
    "structure": STRUCTURE,
    "service": SERVICE,
}
FACT_KEYS = frozenset((
    "what", "value", "unit", "bound", "status", "page", "figure", "spread", "reason", "reading",
    "condition", "quote", "note", "start", "firing",
))  # fmt: skip
KILN_KEYS = frozenset(["name", "design", "doc", "fuel", "draft", "gaps", "notes", *VOCAB])
PAGE = re.compile(r"^(pp?\.\s?\d+([–-]\d+)?)(,\s?pp?\.\s?\d+([–-]\d+)?)*$")
FIGURE = re.compile(r"^(Figs?|Table)\s?[\dA-]")
CLOCK = re.compile(r"^\d{1,2}:\d{2}$")
GIVEN = ("printed", "derived")  # what the book gives, directly or by arithmetic


def load(path: Path = DATA) -> dict[str, Any]:
    """The dataset, as YAML gives it."""
    return cast(dict[str, Any], yaml.safe_load(path.read_text(encoding="utf-8")))


def facts(kiln: dict[str, Any], group: str, what: str, *statuses: str) -> list[Fact]:
    """A kiln's facts of one kind, of the given statuses (any status if none is given)."""
    out: list[Fact] = []
    for f in cast(list[Fact], kiln.get(group) or []):
        if f.get("what") == what and (not statuses or f.get("status") in statuses):
            out.append(f)
    return out


def _is_number(v: object) -> bool:
    return isinstance(v, int | float) and not isinstance(v, bool)


def numeric(f: Fact) -> bool:
    """Whether a fact's value is a number or a [low, high] pair of numbers."""
    v = f.get("value")
    if isinstance(v, list):
        items = cast(list[Any], v)
        return len(items) == 2 and all(_is_number(x) for x in items)
    return _is_number(v)


def raw(f: Fact) -> tuple[float, float]:
    """A numeric fact's value as printed, (low, high), in its own unit (a count unit included)."""
    v = f["value"]
    return (float(v[0]), float(v[1])) if isinstance(v, list) else (float(v), float(v))


def span(f: Fact, unit: str) -> tuple[float, float]:
    """A numeric fact's value as (low, high) in ``unit``; a single value gives the same twice."""
    lo, hi = raw(f)
    return si(Q_(lo, str(f["unit"])), unit), si(Q_(hi, str(f["unit"])), unit)


def label(f: Fact) -> str:
    return str(f.get("firing", ""))


@dataclass(frozen=True)
class Firing:
    """The printed facts of one firing of a kiln: its times and fuels (heat facts by label)."""

    label: str
    times: list[Fact]
    fuels: list[Fact]
    schedules: list[Fact]


def firings(kiln: dict[str, Any]) -> list[Firing]:
    """The kiln's printed (or derived) firings: numeric times and fuels, and printed logs,
    grouped by their label. A time printed in words ("several days") is left out."""
    times = [f for f in facts(kiln, "heat", "firing_time", *GIVEN) if numeric(f)]
    fuels = [f for f in facts(kiln, "heat", "fuel_per_firing", *GIVEN) if numeric(f)]
    logs = facts(kiln, "heat", "schedule", "printed")
    labels = sorted({label(f) for f in times + fuels + logs})
    return [
        Firing(
            x,
            [f for f in times if label(f) == x],
            [f for f in fuels if label(f) == x],
            [f for f in logs if label(f) == x],
        )
        for x in labels
    ]


def burner_inputs(kiln: dict[str, Any]) -> list[tuple[float, str]]:
    """The burners' total input as the book gives it, BTU/hr, with how it was read: a total, or
    else the count times each printed rating (two ratings for one kiln are two readings of the
    book, both kept). Empty if the book doesn't give it."""
    totals = [f for f in facts(kiln, "heat", "burner_input", *GIVEN) if numeric(f)]
    if totals:
        out: list[tuple[float, str]] = []
        for t in totals:
            lo, hi = span(t, "BTU/hr")
            out.append(((lo + hi) / 2, f"{t['status']} total ({t.get('page', '')})"))
        return out
    count = [f for f in facts(kiln, "heat", "burner_count", *GIVEN) if numeric(f)]
    ratings = [f for f in facts(kiln, "heat", "burner_rating", *GIVEN) if numeric(f)]
    if not count:
        return []
    n = raw(count[0])[0]
    each = [(sum(span(r, "BTU/hr")) / 2, r) for r in ratings]
    return [
        (n * e, f"{n:g} burners ({count[0].get('page', '')}) × {e:,.0f} BTU/hr ({r.get('page')})")
        for e, r in each
    ]


def unit_problem(unit: str) -> str | None:
    """Why ``unit`` isn't one the engine's Pint registry (or the count words) knows, or None."""
    if unit in COUNT_UNITS:
        return None
    try:
        ureg.parse_units(unit)
    except pint.UndefinedUnitError, pint.DefinitionSyntaxError, AttributeError, TypeError:
        return f"unit {unit!r} is not one the engine's Pint registry knows"
    return None


def _schedule_problems(where: str, f: Fact) -> list[str]:
    out: list[str] = []
    v = f.get("value")
    if not isinstance(v, list) or not v:
        return [f"{where}: a schedule is a list of ['H:MM', temperature]"]
    for p in cast(list[Any], v):
        pt = cast(list[Any], p) if isinstance(p, list) else []
        if not (len(pt) == 2 and CLOCK.match(str(pt[0])) and _is_number(pt[1])):
            out.append(f"{where}: schedule point {p!r} isn't ['H:MM', number]")
            break
    if f.get("unit") not in {"degC", "degF"}:
        out.append(f"{where}: a schedule's unit is degC or degF")
    return out


def fact_problems(where: str, group: str, f: object) -> list[str]:
    """Everything wrong with one fact: its kind, its source, its status's needs, its value."""
    if not isinstance(f, dict):
        return [f"{where}: a fact must be a mapping"]
    f = cast(Fact, f)
    out: list[str] = []
    if set(f) - FACT_KEYS:
        out.append(f"{where}: unknown keys {sorted(set(f) - FACT_KEYS)}")
    what, status, page = f.get("what"), f.get("status"), f.get("page")
    if what not in VOCAB[group]:
        out.append(f"{where}: what={what!r} is not in the {group} vocabulary")
    if f.get("value") in (None, ""):
        out.append(f"{where}: no value")
    if status not in STATUSES:
        out.append(f"{where}: status={status!r}")
    if status != "assumed" and not page:
        out.append(f"{where}: no page for a {status} value")
    if page and not PAGE.match(str(page)):
        out.append(f"{where}: page {page!r} isn't 'p.N', 'pp.N–M' or a list of them")
    if status in {"scaled", "drawing"} and not f.get("figure"):
        out.append(f"{where}: a {status} value needs its figure")
    if f.get("figure") and not FIGURE.match(str(f["figure"])):
        out.append(f"{where}: figure {f['figure']!r} isn't 'Fig N-M' or 'Table N-M'")
    if status == "scaled" and not f.get("spread"):
        out.append(f"{where}: a scaled value needs its spread")
    if status in {"derived", "assumed"} and not f.get("reason"):
        out.append(f"{where}: a {status} value needs its reason")
    bound = f.get("bound", "=")
    if bound not in BOUNDS:
        out.append(f"{where}: bound {bound!r}")
    if f.get("reading") is not None and f["reading"] not in READINGS:
        out.append(f"{where}: reading {f['reading']!r}")
    if f.get("quote") and len(str(f["quote"]).split()) > 15:
        out.append(f"{where}: a quote is a few words, not {len(str(f['quote']).split())}")
    if what == "schedule":
        return out + _schedule_problems(where, f)
    v, unit = f.get("value"), f.get("unit")
    number = numeric(f)
    if isinstance(v, list) and not number:
        out.append(f"{where}: a list value must be a [low, high] pair of numbers")
    if isinstance(v, list) and number:
        lo, hi = raw(f)
        if lo > hi:
            out.append(f"{where}: range {v} runs backwards")
        if bound != "=":
            out.append(f"{where}: a range can't have a bound")
    unitless = str(what).endswith("_count") or what == "cone"
    if number and not unitless and not unit:
        out.append(f"{where}: a number needs its unit")
    if unit:
        if not number:
            out.append(f"{where}: a unit on a value that isn't a number")
        problem = unit_problem(str(unit))
        if problem:
            out.append(f"{where}: {problem}")
    return out


def problems(data: dict[str, Any]) -> list[str]:
    """Everything wrong with the dataset: each kiln's keys and files, and every fact."""
    out: list[str] = []
    kilns = cast(dict[str, Any], data.get("kilns") or {})
    extras = cast(dict[str, Any], data.get("extras") or {})
    both = [(kid, k, True) for kid, k in kilns.items()] + [
        (kid, k, False) for kid, k in extras.items()
    ]
    for kid, k, modelled in both:
        if not isinstance(k, dict):
            out.append(f"{kid}: not a mapping")
            continue
        k = cast(dict[str, Any], k)
        if set(k) - KILN_KEYS:
            out.append(f"{kid}: unknown keys {sorted(set(k) - KILN_KEYS)}")
        for key in ("name", "design", "doc", "fuel", "draft") if modelled else ("name",):
            if not k.get(key):
                out.append(f"{kid}: no {key}")
        for key in ("design", "doc"):
            if k.get(key) and not (ROOT / str(k[key])).exists():
                out.append(f"{kid}: {key} {k[key]} doesn't exist")
        for group in VOCAB:
            group_facts = k.get(group)
            if group_facts is None:
                continue
            if not isinstance(group_facts, list):
                out.append(f"{kid}.{group}: not a list")
                continue
            for i, f in enumerate(cast(list[Any], group_facts)):
                out += fact_problems(f"{kid}.{group}[{i}]", group, f)
        for key in ("gaps", "notes"):
            items = k.get(key)
            if items is not None and not (
                isinstance(items, list) and all(isinstance(x, str) for x in cast(list[Any], items))
            ):
                out.append(f"{kid}.{key}: a list of strings")
    return out


def assumed(kiln: dict[str, Any]) -> list[str]:
    """What the design file assumes (status assumed), by kind, for the comparison's caveats."""
    out: list[str] = []
    for group in ("chamber", "lining", "flow", "structure"):
        for f in cast(list[Fact], kiln.get(group) or []):
            if f.get("status") == "assumed":
                w = str(f["what"])
                if w not in out:
                    out.append(w)
    return out


def coverage(data: dict[str, Any]) -> dict[str, dict[str, int]]:
    """Counts for the problem set: facts by status, and by kind where the book gives them
    (printed or derived), over the modelled kilns only."""
    by_status: dict[str, int] = {}
    given: dict[str, int] = {}
    kilns_with: dict[str, int] = {}
    for k in cast(dict[str, Any], data["kilns"]).values():
        seen: set[str] = set()
        for group in VOCAB:
            for f in cast(list[Fact], k.get(group) or []):
                s = str(f.get("status"))
                by_status[s] = by_status.get(s, 0) + 1
                if s in GIVEN:
                    key = f"{group}.{f['what']}"
                    given[key] = given.get(key, 0) + 1
                    seen.add(key)
        for key in seen:
            kilns_with[key] = kilns_with.get(key, 0) + 1
    return {"by_status": by_status, "given": given, "kilns_with": kilns_with}
