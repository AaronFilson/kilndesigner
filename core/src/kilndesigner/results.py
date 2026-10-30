"""A simulated firing on disk: Parquet files, read back with DuckDB (ADR 0007).

A run's folder holds:

- ``firing.json``: the summary, its working and findings (:class:`FiringResult`);
- ``series.parquet``: the firing at every step (time, temperatures, powers, energy, cost);
- ``walls.parquet``: every face's cell temperatures through time, long form, one row each:
  run, wall, node, depth_m, layer, time_h, temperature_c.

The CLI, the API and a notebook read the same files. Queries downsample to what a chart can show.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, ConfigDict

from kilndesigner.simulation import FiringPoint, FiringResult, FiringRun

SUMMARY = "firing.json"
SERIES = "series.parquet"
WALLS = "walls.parquet"


def write_run(run: FiringRun, folder: Path, run_id: str = "run") -> list[Path]:
    """Write a run's three files into ``folder``; returns their paths."""
    folder.mkdir(parents=True, exist_ok=True)
    result = run.result
    series = pa.Table.from_pylist([p.model_dump() for p in result.points])
    pq.write_table(series, folder / SERIES)
    columns: dict[str, list[Any]] = {
        k: [] for k in ("run", "wall", "node", "depth_m", "layer", "time_h", "temperature_c")
    }
    for time_h, faces in zip(run.times_h, run.profiles, strict=True):
        for face, temps in zip(result.faces, faces, strict=True):
            n = len(temps)
            columns["run"] += [run_id] * n
            columns["wall"] += [face.face] * n
            columns["node"] += list(range(n))
            columns["depth_m"] += face.depths_m
            columns["layer"] += face.layers
            columns["time_h"] += [time_h] * n
            columns["temperature_c"] += temps
    schema = pa.schema(
        [
            ("run", pa.string()),
            ("wall", pa.string()),
            ("node", pa.int32()),
            ("depth_m", pa.float64()),
            ("layer", pa.string()),
            ("time_h", pa.float64()),
            ("temperature_c", pa.float32()),
        ]
    )
    pq.write_table(pa.table(columns, schema=schema), folder / WALLS, compression="zstd")
    (folder / SUMMARY).write_text(result.model_dump_json(), encoding="utf-8")
    return [folder / SUMMARY, folder / SERIES, folder / WALLS]


def read_summary(folder: Path) -> FiringResult:
    return FiringResult.model_validate_json((folder / SUMMARY).read_bytes())


def _query(sql: str, params: list[object]) -> list[tuple[Any, ...]]:
    with duckdb.connect() as con:
        return con.execute(sql, params).fetchall()


def series(folder: Path, max_points: int = 500) -> list[FiringPoint]:
    """The firing's series, every n-th step so that at most ``max_points`` come back (the last
    step always among them)."""
    path = (folder / SERIES).as_posix()
    rows = _query(
        """
        WITH s AS (SELECT *, row_number() OVER () - 1 AS i, count(*) OVER () AS n
                   FROM read_parquet(?))
        SELECT * EXCLUDE (i, n) FROM s
        WHERE i % greatest(1, ceil(n / ?::DOUBLE)::BIGINT) = 0 OR i = n - 1
        ORDER BY i
        """,
        [path, max_points],
    )
    names = list(FiringPoint.model_fields)
    return [FiringPoint(**dict(zip(names, r, strict=True))) for r in rows]


class WallHeatmap(BaseModel):
    """Each face's temperatures through time: temperatures[t][face][node], °C."""

    model_config = ConfigDict(frozen=True)

    times_h: list[float]
    walls: list[str]
    depths_m: list[list[float]]
    layers: list[list[str]]
    temperatures: list[list[list[float]]]
    min_c: float
    max_c: float


def heatmap(folder: Path, max_times: int = 200) -> WallHeatmap:
    """The walls' temperatures at up to ``max_times`` moments, for the viewer's heatmap."""
    path = (folder / WALLS).as_posix()
    times = [
        r[0]
        for r in _query(
            """
            WITH t AS (SELECT DISTINCT time_h FROM read_parquet(?)),
                 r AS (SELECT time_h, row_number() OVER (ORDER BY time_h) - 1 AS i,
                              count(*) OVER () AS n FROM t)
            SELECT time_h FROM r
            WHERE i % greatest(1, ceil(n / ?::DOUBLE)::BIGINT) = 0 OR i = n - 1
            ORDER BY time_h
            """,
            [path, max_times],
        )
    ]
    walls = _walls_in_order(path)
    depths: list[list[float]] = []
    layers: list[list[str]] = []
    for wall in walls:
        rows = _query(
            "SELECT DISTINCT node, depth_m, layer FROM read_parquet(?) WHERE wall = ? "
            "ORDER BY node",
            [path, wall],
        )
        depths.append([float(r[1]) for r in rows])
        layers.append([str(r[2]) for r in rows])
    rows = _query(
        "SELECT time_h, wall, node, temperature_c FROM read_parquet(?) "
        "WHERE time_h IN (SELECT unnest(?::DOUBLE[])) ORDER BY time_h, node",
        [path, times],
    )
    index = {t: i for i, t in enumerate(times)}
    wall_index = {w: i for i, w in enumerate(walls)}
    grid: list[list[list[float]]] = [[[0.0] * len(d) for d in depths] for _ in times]
    for t, w, node, temp in rows:
        grid[index[t]][wall_index[w]][node] = float(temp)
    lo, hi = _query("SELECT min(temperature_c), max(temperature_c) FROM read_parquet(?)", [path])[0]
    return WallHeatmap(
        times_h=[float(t) for t in times],
        walls=walls,
        depths_m=depths,
        layers=layers,
        temperatures=grid,
        min_c=float(lo),
        max_c=float(hi),
    )


def _walls_in_order(path: str) -> list[str]:
    """The faces as the run wrote them."""
    rows = _query(
        "SELECT wall, min(file_row_number) AS first FROM read_parquet(?, file_row_number = true) "
        "GROUP BY wall ORDER BY first",
        [path],
    )
    return [str(r[0]) for r in rows]
