"""Engine v2's statics: rigid-block limit analysis on the engine's own solids.

Built on build123d (the blocks and their contacts), SciPy's HiGHS (the limit-analysis linear
programs, and the mixed-integer fallback for non-associative friction) and PyNite (the steel
frame), as the user decided on 2026-11-10 (`docs/planning/11-09-26.md` §H;
`docs/research/tool-triples.md` §1).

Heyman's assumptions hold unless a module says otherwise: no tension across a joint, friction at
each joint, compression unlimited except where the hot crushing stand-in applies.
"""
