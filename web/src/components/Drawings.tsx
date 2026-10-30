// The plans' drawings, in the page: the dimensioned sections, then every course plan.
import type { Build } from "@kilndesigner/api-client";
import { useQuery } from "@tanstack/react-query";

import { fileUrl } from "../api";

export const DRAWINGS_INDEX = "drawings/index.json";

interface Drawing {
  file: string;
  kind: "section" | "course plan" | "chart";
  title: string;
  description: string;
}

function Figure({ build, drawing }: { build: Build; drawing: Drawing }) {
  return (
    <figure className="drawing">
      <img src={fileUrl(build.key, `drawings/${drawing.file}`)} alt={drawing.title} />
      <figcaption>
        <strong>{drawing.title}</strong>
        {drawing.description && <span className="muted"> {drawing.description}</span>}
      </figcaption>
    </figure>
  );
}

export function Drawings({ build }: { build: Build }) {
  const drawn = build.files.includes(DRAWINGS_INDEX);
  const index = useQuery({
    queryKey: ["drawings", build.key],
    enabled: drawn,
    staleTime: Infinity, // a build never changes
    queryFn: async () => {
      const response = await fetch(fileUrl(build.key, DRAWINGS_INDEX));
      if (!response.ok) throw new Error(`the drawings could not be loaded (${response.status})`);
      return (await response.json()) as Drawing[];
    },
  });

  if (!drawn) return <p className="muted">This build has no drawings.</p>;
  if (index.isPending) return <p className="muted">Loading the drawings…</p>;
  if (index.isError) return <p className="error">{index.error.message}</p>;
  const of = (kind: Drawing["kind"]) => index.data.filter((d) => d.kind === kind);
  return (
    <div className="drawings">
      {of("section").map((d) => (
        <Figure key={d.file} build={build} drawing={d} />
      ))}
      {of("chart").map((d) => (
        <Figure key={d.file} build={build} drawing={d} />
      ))}
      {of("course plan").length > 0 && (
        <section>
          <h3>Course plans</h3>
          <p className="muted">
            Every brick, course by course, seen from inside the kiln. Cut pieces are orange.
          </p>
          <div className="course-plans">
            {of("course plan").map((d) => (
              <Figure key={d.file} build={build} drawing={d} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
