# Performance review, 28 October 2026

Where the project spends time on a small machine, measured on the 2015 MacBook Pro (2 cores,
4 threads, macOS 12, Colima). The engine was profiled with cProfile over all eight examples; the
times are wall-clock on that machine with nothing else busy. Nothing here has been changed yet.

## What was measured

| What | Time |
|---|---|
| All eight `design_report`s | 9.7 s |
| … with each material's k(T) memoised (an experiment, not in the code) | 4.7 s |
| One plain gas report (gas-crossdraft) | 0.23 s, 1 heat-loss solve |
| One hybrid report (pnw-hybrid-crossdraft) | 2.95 s, 29 heat-loss solves |
| The dome report | 1.32 s, 1 heat-loss solve |
| A full build of gas-crossdraft (report, 3D model, plans), fresh process | 6.8 s, of which 4.4 s is importing build123d |
| Python test suite | 84–150 s |
| Web test suite | 35–42 s, a third of it creating jsdom |

## The engine, by size of the win

1. **Memoise each material's k(T).** `Material.k` calls `ConductivityData.to_conductivity()`,
   which converts every data-sheet point through Pint, on every call. The heat-loss solver calls
   it 7,069 times for the eight examples: 9.4 s of a 17.4 s profile. Memoised, the eight reports
   took 4.7 s instead of 9.7 s. The data is frozen, so a cache keyed on the unit, temperature unit
   and points (or converting once when the library loads) is safe. `library.py:26`, `:57`.
2. **Keep Pint out of the hot loops.** `units.si()` runs 66,202 times for the eight reports
   (7.6 s cumulative); each `Quantity.to()` costs about 0.1 ms here. ADR 0004 already has the
   solvers take SI floats; the heat-loss and hybrid code still convert inside loops. Convert once
   per solve.
3. **Solve the hybrid's heat loss on one grid.** `analyse_hybrid` runs a full heat-loss solve for
   each 100 °F cost point (about 21) and again inside the root search for the electric ceiling
   (about 7): 29 per hybrid report. The cost grid's losses bracket the ceiling already; finding it
   from them, then polishing with two or three solves, saves most of the search.
   `hybrid.py:95-105, 141`.
4. **Cache the dome's area.** `SailDome.area(depth)` sums a 400 × 400 grid on every call, and the
   wall solver's integral of 1/A(x) calls it about 30 times a layer: 297 calls, 1.0 s of the dome
   report's 1.3 s. Cache it by depth, or tabulate A at a few depths and interpolate (A is smooth).
   `shape.py:170`.
5. **Invert the Kirchhoff integral exactly.** `Conductivity.upper_temperature` finds each layer's
   far-side temperature with a root search to 1e-9 K, evaluating ∫k dT about ten times a step
   (14,231 searches, 145,631 integrals, 2.1 s). k(T) is piecewise linear, so ∫k dT is piecewise
   quadratic and inverts in closed form, segment by segment. `thermal/conductivity.py:64`.
6. **Compute each face's ∫dx/A(x) once.** `_depth_integrals` doesn't depend on temperature, but
   runs on every solve (1.1 s cumulative). Cache it per face. `thermal/wall.py:54`.

Items 1, 3 and 5 also speed up the slowest tests (each hybrid test takes 2–4 s).

## Builds and the worker

7. **Warm the geometry imports at worker start.** The first build in a process spends 4.4 s
   importing build123d, which pulls in scikit-learn (1.4 s) and scipy.stats (1.0 s). The model
   and its STEP/glTF export take about 1.7 s after that. `build_design` imports lazily, so the
   first build after each worker start is the slow one; importing `kilndesigner.geometry` in the
   worker's `on_startup` moves the cost to when nobody is waiting.
8. **Every engine edit rebuilds every design.** The build key includes a hash of every engine
   `.py` and `.yaml` file (`build.py:29`), so any edit, even a comment, re-keys every saved design,
   and each one rebuilds (about 7 s here) when next opened. On this machine, during development,
   that's a rebuild storm. Separate fingerprints for the report and for the model and plans would
   keep most rebuilds to the cheap half. That's a decision for ADR 0008.

## Tests

9. **Python:** after items 1–6, measure again. Most of the remaining time is OpenCascade and full
   reports in the API and CLI tests (`compare` builds two reports: 6.8 s). pytest-xdist with two
   workers would use the second core; memory (16 GB) isn't the limit.
10. **Web:** Vitest reports "jsdom was created 10 times · 30 s total, 31 % of tracked time", and
    suggests `pool: 'vmThreads'` or `isolate: false`. The first keeps each file isolated; the
    second is faster but shares globals between files, which these tests stub and restore. Set it
    in `web/vite.config.ts`'s `test` block, with `maxWorkers: 2` on this machine.

## The dev loop on this Mac

11. **Drop `--force` from Vite.** The running dev server was started as `vite --force`, which
    re-bundles three.js, drei and CodeMirror at every start. That's slow here, and a dependency
    rebuild is what mixed old and new chunks in the 27 October viewer failure. Use `--force` only
    after a dependency changes.
12. **The Colima VM costs CPU while idle.** Its QEMU process sat at 14 % CPU and about 710 MB
    resident with the app idle, on a 2-core machine. Stop it when the app isn't in use
    (`scripts/colima.sh stop`), or run Postgres and Valkey natively (Homebrew) and skip the VM.
13. **Load the 3D viewer and the YAML editor lazily.** `KilnViewer` (three.js, drei) and
    `YamlEditor` (CodeMirror) are imported eagerly, so every page parses them. `React.lazy` for
    both would cut the first load on an old machine. Not measured.
