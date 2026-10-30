# 5. Geometry is built only in Python (build123d) and served as glTF

- **Status:** proposed
- **Date:** 2026-10-21

## Context

The kiln must be viewable in a browser, exportable to CAD (STEP) and drawn as plans (DXF, PDF).
Building geometry in both Python and JavaScript would mean two models that disagree.

## Decision

- build123d (on OpenCascade) builds a B-rep model from the `Kiln`: each brick course, layer, arch,
  port and the shell are named solids.
- The same model is exported as STEP (CAD), STL (printing scale models), DXF and SVG (plans), and
  glTF binary (the viewer). glTF nodes carry the part id, so the viewer can select a part and
  show its working.
- Exports are cached by a hash of the design, so an unchanged design is never rebuilt.

## Consequences

- One source of truth for geometry; the browser only displays it.
- A change in the editor needs a round trip to the server, which takes from 100 ms to a few
  seconds. The editor shows the previous model until the new one arrives. Simple changes, such
  as moving the camera or hiding a layer, stay in the browser.
- OpenCascade wheels are large; the API and worker images are bigger than a plain Python image.

## In an interview

"Python owns the geometry. The browser gets glTF with part ids, so clicking a brick in the
viewer can show the calculation behind it, and the plans come from the same solids as the 3D
view."
