// A small SVG line chart: axes with round ticks, a legend, and a marker at a chosen x.
import { extent, linePath, type Series, ticks } from "../firing";

const W = 560;
const H = 200;
const PAD = { left: 52, right: 12, top: 10, bottom: 30 };

export function LineChart({
  title,
  xLabel,
  yLabel,
  series,
  marker,
}: {
  title: string;
  xLabel: string;
  yLabel: string;
  series: Series[];
  marker?: number;
}) {
  const xs = extent(series, 0, false);
  const ys = extent(series, 1);
  const w = W - PAD.left - PAD.right;
  const h = H - PAD.top - PAD.bottom;
  const px = (x: number) => ((x - xs[0]) / (xs[1] - xs[0])) * w;
  const py = (y: number) => h - ((y - ys[0]) / (ys[1] - ys[0])) * h;
  return (
    <figure className="chart">
      <figcaption>{title}</figcaption>
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={title}>
        <g transform={`translate(${PAD.left},${PAD.top})`}>
          {ticks(ys[0], ys[1]).map((t) => (
            <g key={`y${t}`}>
              <line x1={0} x2={w} y1={py(t)} y2={py(t)} className="grid" />
              <text x={-6} y={py(t)} textAnchor="end" dominantBaseline="middle">
                {t.toLocaleString()}
              </text>
            </g>
          ))}
          {ticks(xs[0], xs[1]).map((t) => (
            <text key={`x${t}`} x={px(t)} y={h + 16} textAnchor="middle">
              {t.toLocaleString()}
            </text>
          ))}
          {series.map((s) => (
            <path
              key={s.label}
              d={linePath(s.points, xs, ys, w, h)}
              fill="none"
              stroke={s.colour}
              strokeWidth={2}
              strokeDasharray={s.dashed ? "5 4" : undefined}
            >
              <title>{s.label}</title>
            </path>
          ))}
          {marker !== undefined && (
            <line x1={px(marker)} x2={px(marker)} y1={0} y2={h} className="marker" data-testid="marker" />
          )}
          <text x={w / 2} y={h + 28} textAnchor="middle" className="axis-label">
            {xLabel}
          </text>
          <text transform={`translate(-44,${h / 2}) rotate(-90)`} textAnchor="middle" className="axis-label">
            {yLabel}
          </text>
        </g>
      </svg>
      <ul className="legend">
        {series.map((s) => (
          <li key={s.label}>
            <span className="swatch" style={{ background: s.colour }} /> {s.label}
          </li>
        ))}
      </ul>
    </figure>
  );
}
