// The API, as TanStack Query hooks over the generated client.
import { createClient, type Build, type Problem } from "@kilndesigner/api-client";
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

export const fileUrl = (key: string, name: string) =>
  `/api/builds/${key}/files/${encodeURIComponent(name)}`;

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
    mutationFn: async (source: string) => {
      const { data, error, response } = await api.POST("/api/designs", { body: { source } });
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
    mutationFn: async (source: string) => {
      const { data, error, response } = await api.POST("/api/designs/{design_id}/versions", {
        params: { path: { design_id: id } },
        body: { source },
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
export function useBuild(key: string) {
  return useQuery({
    queryKey: ["builds", key],
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

export function useReport(build: Build) {
  return useQuery({
    queryKey: ["reports", build.key],
    enabled: build.status === "done" && build.files.includes("report.json"),
    staleTime: Infinity, // a build never changes
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/builds/{key}/report", {
        params: { path: { key: build.key } },
      });
      return data ?? fail(response, error);
    },
  });
}
