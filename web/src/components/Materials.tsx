// What to buy and what to cut: the bill of materials and the brick cut list.
import type { Report } from "@kilndesigner/api-client";

import { Findings } from "./ReportView";

const money = (value: number) =>
  value.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

export function Materials({ report }: { report: Report }) {
  const { bom, masonry } = report;
  if (!bom) return <p className="muted">This design has no bill of materials.</p>;
  const names = new Map(masonry?.quantities.map((q) => [q.material, q.name]));
  return (
    <div className="materials">
      <table>
        <caption>Bill of materials</caption>
        <thead>
          <tr>
            <th scope="col">Item</th>
            <th scope="col">Needed</th>
            <th scope="col">Buy</th>
            <th scope="col">Price</th>
            <th scope="col" className="number">
              Cost
            </th>
          </tr>
        </thead>
        <tbody>
          {bom.lines.map((line) => (
            <tr key={line.item}>
              <th scope="row">{line.item}</th>
              <td>{line.needed}</td>
              <td>{line.buy}</td>
              <td>{line.unit_price ?? "—"}</td>
              <td className="number">{line.cost == null ? "not priced" : money(line.cost)}</td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr>
            <th scope="row" colSpan={4}>
              Total of the priced items (prices checked {bom.prices_checked})
            </th>
            <td className="number">{money(bom.total)}</td>
          </tr>
        </tfoot>
      </table>
      <Findings findings={bom.findings} />
      {masonry && masonry.cut_list.length > 0 && (
        <table>
          <caption>Cut list</caption>
          <thead>
            <tr>
              <th scope="col">Brick</th>
              <th scope="col">Cut</th>
              <th scope="col" className="number">
                Pieces
              </th>
            </tr>
          </thead>
          <tbody>
            {masonry.cut_list.map((line) => (
              <tr key={`${line.material} ${line.cut}`}>
                <th scope="row">{names.get(line.material) ?? line.material}</th>
                <td>{line.cut}</td>
                <td className="number">{line.count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
