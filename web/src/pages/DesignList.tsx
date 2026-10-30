import { Link } from "@tanstack/react-router";

import { useDesigns } from "../api";

export function DesignList() {
  const designs = useDesigns();
  return (
    <main className="page">
      <header className="page-header">
        <h1>Designs</h1>
        <Link to="/designs/new" className="button">
          New design
        </Link>
      </header>
      {designs.isPending && <p className="muted">Loading…</p>}
      {designs.isError && <p className="error">{designs.error.message}</p>}
      {designs.data?.length === 0 && (
        <p className="muted">No designs yet. Start one from a design file (YAML).</p>
      )}
      <ul className="design-list">
        {designs.data?.map((d) => (
          <li key={d.id}>
            <Link to="/designs/$designId" params={{ designId: d.id }}>
              {d.name}
            </Link>
            <time dateTime={d.updated_at}>{new Date(d.updated_at).toLocaleString()}</time>
          </li>
        ))}
      </ul>
    </main>
  );
}
