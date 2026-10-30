import type { Problem } from "@kilndesigner/api-client";

/** Where a problem is in the design, as a path: `chamber.width`, `lining.walls[0]`. */
export function where(loc: Problem["loc"]): string {
  return loc.reduce<string>(
    (path, part) =>
      typeof part === "number" ? `${path}[${part}]` : path ? `${path}.${part}` : part,
    "",
  );
}

export function Problems({ problems }: { problems: Problem[] }) {
  if (problems.length === 0) return null;
  return (
    <ul className="problems" role="alert">
      {problems.map((p, i) => (
        <li key={i}>
          {p.loc.length > 0 && <code>{where(p.loc)}</code>} {p.msg}
        </li>
      ))}
    </ul>
  );
}
