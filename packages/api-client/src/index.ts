// A typed client for the Kilndesigner API. The types come from openapi.json, which the Python
// tests keep in step with the API; regenerate with `npm run generate`.
import createFetchClient from "openapi-fetch";

import type { components, paths } from "./schema";

export type { components, paths };
export type Schemas = components["schemas"];
export type Design = Schemas["Design"];
export type DesignSummary = Schemas["DesignSummary"];
export type Version = Schemas["Version"];
export type Build = Schemas["Build"];
export type Problem = Schemas["Problem"];
export type Report = Schemas["Report"];
export type Finding = Schemas["Finding"];
export type Step = Schemas["Step"];

export function createClient(baseUrl = "") {
  return createFetchClient<paths>({ baseUrl });
}

export type Client = ReturnType<typeof createClient>;
