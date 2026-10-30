"""Line charts for the plans: plain SVG, positions worked out from the chart's fixed layout."""

from xml.etree import ElementTree

import pytest

from kilndesigner.charts import PALETTE, Marker, Series, line_chart

SVG = "{http://www.w3.org/2000/svg}"
# The default 640 × 300 chart keeps 64 px on the left, 16 right, 16 top and 46 at the bottom:
# a plot 560 px wide and 238 px high.
LEFT, TOP, PLOT_W, PLOT_H = 64.0, 16.0, 560.0, 238.0


def _parse(svg: str) -> ElementTree.Element:
    return ElementTree.fromstring(svg)


def _texts(root: ElementTree.Element) -> list[str]:
    return [t.text or "" for t in root.iter(f"{SVG}text")]


@pytest.mark.parametrize(
    ("lo", "hi", "expected"),
    [
        # The x axis gets about six ticks: (12 - 0) / 6 = 2, a round step already
        (0.0, 12.0, ["0", "2", "4", "6", "8", "10", "12"]),
        # 1.2 / 6 = 0.2: 2 × 0.1
        (0.0, 1.2, ["0", "0.2", "0.4", "0.6", "0.8", "1", "1.2"]),
        # 15 / 6 = 2.5: 1 and 2 are too small, so 2.5 × 1
        (0.0, 15.0, ["0", "2.5", "5", "7.5", "10", "12.5", "15"]),
        # 6 / 6 = 1, from the whole number below 3.5, which is left off
        (3.5, 9.5, ["4", "5", "6", "7", "8", "9"]),
    ],
)
def test_ticks_are_round_steps_inside_the_range(lo: float, hi: float, expected: list[str]) -> None:
    root = _parse(line_chart([Series("a", [(lo, 1), (hi, 2)])], x_label="x", y_label="y"))
    # x tick labels sit 16 px under the plot
    under = f"{TOP + PLOT_H + 16}"
    assert [t.text for t in root.iter(f"{SVG}text") if t.get("y") == under] == expected


def test_a_series_is_drawn_across_the_plot() -> None:
    root = _parse(line_chart([Series("Kiln", [(0, 0), (10, 5)])], x_label="t", y_label="kW"))
    assert root.get("viewBox") == "0 0 640 300"
    (line,) = root.iter(f"{SVG}polyline")
    # x: 0 at the plot's left edge, 10 at its right. y: the axis runs 0 to 5 × 1.08 = 5.4, so
    # 0 sits on the plot's bottom (16 + 238 = 254) and 5 at 254 - 5 / 5.4 × 238 = 33.6.
    assert line.get("points") == "64.0,254.0 624.0,33.6"
    assert line.get("stroke") == PALETTE[0]
    assert line.get("stroke-dasharray") is None
    texts = _texts(root)
    # y ticks: 5.4 / 5 = 1.08 per tick, rounded up to 2; x ticks: 10 / 6 = 1.67, also 2
    assert texts[:3] == ["0", "2", "4"]
    assert texts[3:9] == ["0", "2", "4", "6", "8", "10"]
    assert {"Kiln", "t", "kW"} <= set(texts)


def test_no_zero_line_when_the_axis_starts_at_zero() -> None:
    root = _parse(line_chart([Series("a", [(0, 0), (10, 5)])], x_label="x", y_label="y"))
    assert not [x for x in root.iter(f"{SVG}line") if x.get("stroke") == "#555"]


def test_a_zero_line_when_values_go_below_zero() -> None:
    root = _parse(line_chart([Series("a", [(0, -2), (10, 4)])], x_label="x", y_label="y"))
    (zero,) = [x for x in root.iter(f"{SVG}line") if x.get("stroke") == "#555"]
    # The axis runs -2 to 4 × 1.08 = 4.32, so 0 is 2 / 6.32 of the way up the 238 px plot
    expected = TOP + PLOT_H - 2 / 6.32 * PLOT_H
    assert float(zero.get("y1", "")) == pytest.approx(expected, abs=0.05)
    assert zero.get("x1") == str(LEFT)
    assert zero.get("x2") == str(LEFT + PLOT_W)
    assert _texts(root)[:4] == ["-2", "0", "2", "4"]


def test_markers_are_dashed_lines_with_their_label() -> None:
    root = _parse(
        line_chart(
            [Series("a", [(0, 1), (10, 2)])],
            x_label="x",
            y_label="y",
            markers=[Marker(5, "switch-over, 1650 °F & <hand over>")],
        )
    )
    (marker,) = [x for x in root.iter(f"{SVG}line") if x.get("stroke") == "#2e7d32"]
    assert marker.get("x1") == marker.get("x2") == f"{LEFT + PLOT_W / 2:.1f}"
    assert marker.get("y1") == str(TOP)
    assert marker.get("y2") == str(TOP + PLOT_H)
    assert marker.get("stroke-dasharray") == "4 3"
    assert "switch-over, 1650 °F & <hand over>" in _texts(root)


def test_y_ticks_use_the_format_given() -> None:
    root = _parse(
        line_chart([Series("a", [(0, 0), (10, 0.1)])], x_label="x", y_label="y", y_format="${:.3f}")
    )
    # The axis runs to 0.1 × 1.08 = 0.108: 0.0216 per tick, rounded up to 0.025
    assert _texts(root)[:5] == ["$0.000", "$0.025", "$0.050", "$0.075", "$0.100"]


def test_dashed_series_and_colours_cycling_through_the_palette() -> None:
    series = [Series(f"s{i}", [(0, i + 1), (1, i + 2)], dashed=i == 1) for i in range(5)]
    root = _parse(line_chart(series, x_label="x", y_label="y"))
    lines = list(root.iter(f"{SVG}polyline"))
    assert [x.get("stroke") for x in lines] == [*PALETTE, PALETTE[0]]
    assert [x.get("stroke-dasharray") for x in lines] == [None, "6 4", None, None, None]
    # each series has a legend swatch in its colour, dashed like its line, and its label
    swatches = [x for x in root.iter(f"{SVG}line") if x.get("stroke-width") == "2"]
    assert [x.get("stroke") for x in swatches] == [x.get("stroke") for x in lines]
    assert [x.get("stroke-dasharray") for x in swatches] == [None, "6 4", None, None, None]
    assert [f"s{i}" for i in range(5)] == [t for t in _texts(root) if t.startswith("s")]
