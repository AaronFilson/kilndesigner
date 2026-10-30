# 10. The web app is React with React Three Fiber

- **Status:** proposed
- **Date:** 2026-10-21

## Context

The web app is mostly a 3D viewer and a form-heavy editor. Angular and React are already shown
in other projects; what's new here is 3D in the browser.

## Decision

- React 19, Vite, TanStack Router and Query, and the OpenAPI-generated client, as in Studio
  Manager.
- React Three Fiber and drei for the viewer: glTF loading, part picking, section planes, exploded
  views by course, and a temperature heatmap as a custom shader driven by simulation results.
- Plans open as PDFs. The editor shows each derived value with a link to its working.

## Consequences

- Effort goes into the 3D work, not into learning another framework.
- The heatmap shader needs a WebGL2 fallback where WebGPU isn't available.

## In an interview

"I kept a framework I know so the new work was the 3D: a React Three Fiber viewer with picking,
section cuts and a shader heatmap of the firing simulation."
