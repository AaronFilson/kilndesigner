# 14. Built kilns are the reference: a rule that fails one is the rule's fault

- **Status:** proposed
- **Date:** 2026-10-29

## Context

The engine's rules came from several sources: rules of thumb (Olsen, Ward, Rhodes), industrial
practice (HarbisonWalker's arch tables), makers' ratings and physics. Read against the kilns
Olsen describes in *The Kiln Book* (4th ed.), several of them refused or flagged kilns that are
built and fired. The fast-fire kiln's No. 1 arch, 4½ in of insulating brick over 27 in at 1½ in
per foot, failed two arch errors. His 4–6 in/ft chamber-kiln arches failed the rise rule. His
100 ft³ updraft's flue was under the 2½ in² per ft³ the engine required. His 36 ft³ cross-draft,
fired to cone 10 on 6,000 BTU/ft³/hr, was short of the burner input the engine demanded.

## Decision

- The kilns the book describes are designs in `examples/olsen/`, and the engine must build every
  one without an error (`core/tests/test_olsen_kilns.py`). A warning that remains must say
  something true about the kiln as built, and is listed in the test with why.
- **Errors are for physics.** A kiln is refused when it can't work, not when it departs from a
  rule of thumb:
  - the burners' available heat at the top temperature must cover the lining's steady loss;
  - a skewback must have a wall under it;
  - hot steel must stay within its allowable stress.
- **Rules of thumb give starting sizes**, and warn only past the edge of what the book states
  and builds. This covers the chimney's height, the exit flue, the grate against the chimney and
  the burner input. Olsen builds these parts to be tuned (p.81, Principle 9).
- **Industrial rules become notes where the book's kilns contradict them.**
  - HarbisonWalker's 1–3 in/ft rise is replaced by Olsen's least rise, 1½ in/ft (p.51), a
    warning. He sets no most.
  - Past HarbisonWalker's heated-arch method (a ring too thick for its rise), the steel takes
    5.34 × the cold thrust, the largest factor the table prints. That reproduces the
    2 × 2 × 3/16 in frame Olsen bolts on his fast-fire kiln (p.139).
  - "Never a stretcher course under the skewback" is a note: Olsen's IFB kilns lay one.
- **Defaults follow Olsen.**
  - Burners are sized by his Rule 1, 10,000 BTU/ft³/hr for insulating brick (Ward's slow end),
    with Ward's fast end on request.
  - A gas kiln's chimney reaches the kiln's top, with a hood and stack (p.151).
  - The exit flue starts as large as the burner ports (p.151).
  - Elements are designed at his 9 W/in² (p.254, p.257).

## Consequences

- Designs that were refused now build, and say why they work: a note names the rule they depart
  from and the kiln in the book that does the same.
- A new rule needs a reference kiln it passes, or it can only warn.
- Where a book kiln leaves out what the engine needs (walls, burners), its design states the
  assumption, and the assumption is chosen from Olsen's own recommendations.
