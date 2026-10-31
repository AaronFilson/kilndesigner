// The API, as TanStack Query hooks over the generated client.
import {
  createClient,
  type Build,
  type Problem,
  type Simulation,
  type SwitchOverChart,
} from "@kilndesigner/api-client";

import type { KilnDocument, Layout } from "./design";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export const api = createClient();

/** A request the API refused. `problems` says where and why, when the design was not valid. */
export class ApiError extends Error {
  constructor(
    readonly status: number,
    message: string,
    readonly problems: Problem[] = [],
  ) {
    super(message);
  }
}

function fail(response: Response, error: unknown): never {
  const detail = (error as { detail?: unknown } | undefined)?.detail;
  if (Array.isArray(detail)) {
    throw new ApiError(response.status, "The design is not valid", detail as Problem[]);
  }
  throw new ApiError(response.status, typeof detail === "string" ? detail : response.statusText);
}

/** A file a build wrote, by its path in the build: `plans.pdf`, `drawings/view-1.svg`. */
export const fileUrl = (key: string, name: string) =>
  `/api/builds/${key}/files/${name.split("/").map(encodeURIComponent).join("/")}`;

/** A design to save or check: the YAML (the file, or the YAML tab) or the document (the form). */
export type DesignInput = { source: string } | { document: KilnDocument };

function body(input: DesignInput) {
  return "source" in input
    ? { source: input.source }
    : { document: input.document as unknown as Record<string, unknown> };
}

/** Check a design without saving it; the result is the design both ways. */
export async function checkDesign(input: DesignInput) {
  const { data, error, response } = await api.POST("/api/designs/check", { body: body(input) });
  return data ? { ...data, document: data.document as unknown as KilnDocument } : fail(response, error);
}

export function useTemplates() {
  return useQuery({
    queryKey: ["templates"],
    staleTime: Infinity,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/templates");
      return data ?? fail(response, error);
    },
  });
}

export function useLibrary() {
  return useQuery({
    queryKey: ["library"],
    staleTime: Infinity,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/library");
      return data ?? fail(response, error);
    },
  });
}

export function useDesigns() {
  return useQuery({
    queryKey: ["designs"],
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/designs");
      return data ?? fail(response, error);
    },
  });
}

export function useDesign(id: string) {
  return useQuery({
    queryKey: ["designs", id],
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/designs/{design_id}", {
        params: { path: { design_id: id } },
      });
      return data ?? fail(response, error);
    },
  });
}

export function useCreateDesign() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (input: DesignInput) => {
      const { data, error, response } = await api.POST("/api/designs", { body: body(input) });
      return data ?? fail(response, error);
    },
    onSuccess: (design) => {
      client.setQueryData(["designs", design.id], design);
      void client.invalidateQueries({ queryKey: ["designs"], exact: true });
    },
  });
}

export function useSaveVersion(id: string) {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (input: DesignInput) => {
      const { data, error, response } = await api.POST("/api/designs/{design_id}/versions", {
        params: { path: { design_id: id } },
        body: body(input),
      });
      return data ?? fail(response, error);
    },
    onSuccess: (design) => {
      client.setQueryData(["designs", id], design);
      void client.invalidateQueries({ queryKey: ["designs"], exact: true });
    },
  });
}

export function useDeleteDesign() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { error, response } = await api.DELETE("/api/designs/{design_id}", {
        params: { path: { design_id: id } },
      });
      if (!response.ok) fail(response, error);
    },
    onSuccess: () => client.invalidateQueries({ queryKey: ["designs"] }),
  });
}

const finished = (build: Build | null | undefined) =>
  build != null && (build.status === "done" || build.status === "failed");

/** A build, polled while it runs. `null` means it has not been started. */
export function useBuild(key: string, enabled = true) {
  return useQuery({
    queryKey: ["builds", key],
    enabled,
    queryFn: async (): Promise<Build | null> => {
      const { data, error, response } = await api.GET("/api/builds/{key}", {
        params: { path: { key } },
      });
      if (response.status === 404) return null;
      return data ?? fail(response, error);
    },
    refetchInterval: (query) =>
      query.state.data === null || finished(query.state.data) ? false : 1000,
  });
}

export function useStartBuild() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (key: string) => {
      const { data, error, response } = await api.POST("/api/builds/{key}", {
        params: { path: { key } },
      });
      return data ?? fail(response, error);
    },
    onSuccess: (build) => client.setQueryData(["builds", build.key], build),
  });
}

/** Where a build put each port, and each wall's frame; undefined for a build without one. */
export function useLayout(build: Build | null | undefined) {
  return useQuery({
    queryKey: ["layouts", build?.key],
    enabled: build?.status === "done" && build.files.includes("layout.json"),
    staleTime: Infinity, // a build never changes
    queryFn: async () => {
      const response = await fetch(fileUrl(build?.key ?? "", "layout.json"));
      if (!response.ok) throw new ApiError(response.status, response.statusText);
      return (await response.json()) as Layout;
    },
  });
}

const settled = (sim: Simulation | null | undefined) =>
  sim != null && (sim.status === "done" || sim.status === "failed");

/** A simulated firing of a design version, polled while it runs. `null`: not started. */
export function useSimulation(key: string) {
  return useQuery({
    queryKey: ["simulations", key],
    queryFn: async (): Promise<Simulation | null> => {
      const { data, error, response } = await api.GET("/api/simulations/{key}", {
        params: { path: { key } },
      });
      if (response.status === 404) return null;
      return data ?? fail(response, error);
    },
    refetchInterval: (query) => (query.state.data === null || settled(query.state.data) ? false : 1000),
  });
}

export function useStartSimulation() {
  const client = useQueryClient();
  return useMutation({
    mutationFn: async (key: string) => {
      const { data, error, response } = await api.POST("/api/simulations/{key}", {
        params: { path: { key } },
      });
      return data ?? fail(response, error);
    },
    onSuccess: (sim) => client.setQueryData(["simulations", sim.key], sim),
  });
}

/** A slow firing over a time the user chooses (`kilndesigner slow`), worked out on request. */
export function useSlowFiring() {
  return useMutation({
    mutationFn: async ({ key, time, soak }: { key: string; time: string; soak: string }) => {
      const { data, error, response } = await api.POST("/api/simulations/{key}/slow", {
        params: { path: { key } },
        body: { time, soak },
      });
      return data ?? fail(response, error);
    },
  });
}

/** A finished firing's results: its summary, its series, the walls' heatmap and, for a hybrid, the
 * switch-over chart (null when the kiln has none). A finished run never changes. */
export function useFiring(key: string) {
  const path = { params: { path: { key } } };
  const result = useQuery({
    queryKey: ["firing", key, "result"],
    staleTime: Infinity,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/simulations/{key}/result", path);
      return data ?? fail(response, error);
    },
  });
  const series = useQuery({
    queryKey: ["firing", key, "series"],
    staleTime: Infinity,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/simulations/{key}/series", {
        params: { path: { key }, query: { max_points: 400 } },
      });
      return data ?? fail(response, error);
    },
  });
  const heatmap = useQuery({
    queryKey: ["firing", key, "heatmap"],
    staleTime: Infinity,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/simulations/{key}/heatmap", {
        params: { path: { key }, query: { max_times: 120 } },
      });
      return data ?? fail(response, error);
    },
  });
  const switchover = useQuery({
    queryKey: ["firing", key, "switchover"],
    staleTime: Infinity,
    queryFn: async (): Promise<SwitchOverChart | null> => {
      const { data, error, response } = await api.GET("/api/simulations/{key}/switchover", path);
      if (response.status === 404) return null;
      return data ?? fail(response, error);
    },
  });
  return { result, series, heatmap, switchover };
}

/** Whether a build has a report to load: one that finished and wrote it. */
export function hasReport(build: Build): boolean {
  return build.status === "done" && build.files.includes("report.json");
}

export function useReport(build: Build) {
  return useQuery({
    queryKey: ["reports", build.key],
    enabled: hasReport(build),
    staleTime: Infinity, // a build never changes
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/builds/{key}/report", {
        params: { path: { key: build.key } },
      });
      return data ?? fail(response, error);
    },
  });
}
