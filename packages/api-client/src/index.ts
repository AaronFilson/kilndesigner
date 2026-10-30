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
export type Check = Schemas["Check"];
export type Cell = Schemas["Cell"];
export type Requirement = Schemas["Requirement"];
export type Step = Schemas["Step"];
export type Template = Schemas["Template"];
export type Library = Schemas["Library"];
export type CheckedDesign = Schemas["CheckedDesign"];
export type Simulation = Schemas["Simulation"];
export type FiringResult = Schemas["FiringResult"];
export type FiringPoint = Schemas["FiringPoint"];
export type WallHeatmap = Schemas["WallHeatmap"];
export type SwitchOverChart = Schemas["SwitchOverChart"];
export type SwitchPoint = Schemas["SwitchPoint"];

export function createClient(baseUrl = "") {
  return createFetchClient<paths>({ baseUrl });
}

export type Client = ReturnType<typeof createClient>;
