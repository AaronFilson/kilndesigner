# Steel for a door under a dome: lintels, frames and the dome's steel

Checked: 2026-10-30. Scope: the steel round a door in a wall that a sail dome or a cast dome
bears on, and the steel that holds the dome's thrust. It gathers what the repo already holds
(`door-headers.md`, `domes-over-doors.md`, `kiln-reference.md`, `olsen-kilns.md`) and states the
method the engine uses. Marks as in `door-headers.md`: Verified, Excerpt, Derived, NOT FOUND.
No new external source was read for this note; every number traces to one already in the repo.

---

## S1. How built dome kilns span their doors (ADR 0014: built kilns are the reference)

Olsen, *The Kiln Book*, 4th ed. (the user's copy; pages as in `olsen-kilns.md`):

| Kiln | What carries the roof over the door | Page | Mark |
|---|---|---|---|
| Kanayama multi-directional (`kanayama-multi`) | "Ring-arch doors on arch frames, one per firebox"; 9 in walls; outside walls buttressed with dirt, rocks and concrete; dome cast 5–6 in thick | pp.186–188 | Read (`olsen-kilns.md`) |
| Gulgong racer (`gulgong-racer`) | Cast dome (Coolcast 140); walls buttressed with concrete and rocks | pp.119–120 | Read |
| Höhr-Grenzhausen anagama-style (`hohr-2003`) | Cast dome "buttressed with concrete, rocks and rubble" | p.123 | Read |
| A wood kiln with "supporting wall in front of all doors" | Arched doors, bricked up; a supporting wall in front | Fig 4-15 | Read (sizes unreadable) |
| Miravet (`miravet`) | Dome over an 8 × 8 ft cube; walls 3–4 ft thick, partly buried | p.158 | Read |
| Breda bottle kiln (`breda-bottle`) | 2 ft wall "with metal banding" under a domed ceiling | p.167 | Read |
| Early domed and beehive kilns | walls 18–22 in thick, some 3–5 ft, "carried the thrust of the dome without reinforcing" | p.45 | Read (`kiln-reference.md` §1) |
| Climbing kiln | "The door arch frame support is made to span the door jamb, and the door ring arch is laid"; "steel supports must be used" where skewback, wall and arch form an acute angle | — | Excerpt [H11] |
| Updraft 5 × 5 × 6 ft (sprung arch) | door frame 3 × 3 × ¼ in angle; "can be larger (stronger), but not smaller" | p.174 | Read |
| Any | "A heavy door on undersized angle iron can torque the arch and break its bond" | p.175 | Read |

So the built dome kilns span their doors with **a ring (door) arch on a form, set in a wall that
is buttressed by earth, rock and concrete or by thick masonry**, or band the kiln with iron.
**None in Olsen spans a door under a dome with a steel lintel**, and none gives a door arch's or a
lintel's size. Elsewhere in the repo: the Brazilian beehive kiln puts "a steel plate or pieces of
bamboo" across its door columns and lays the wall over them, with "one steel band for dome"
(`domes-over-doors.md` [D11], Verified); a bottle oven's wicket has "a stout iron frame" [D18]
(secondary); Pike & Schopp's 1886 kiln has "an arched iron frame" at the door with the bands
fastened over it [D17] (Verified).

## S2. Steel strength: AISC 360-16 (already Verified in `door-headers.md` §D2 [H7])

- A36: Fy = 36 ksi; E = 29,000 ksi. ASD bending Ω_b = 1.67 (§F1).
- §F10 single angles: yielding Mn = 1.5My (F10-1); lateral-torsional buckling F10-2/F10-3 with
  Mcr from F10-5a for an equal-leg angle bent about a geometric axis with no LTB restraint, toe
  in compression, My = 0.80 × the geometric yield moment; leg local buckling F10-6 (noncompact),
  F10-7/8 (slender), Sc = 0.80 Sx; λp = 0.54√(E/Fy), λr = 0.91√(E/Fy) (Table B4.1b case 12).
- The engine's F10 chain reproduces `door-headers.md` §D2's worked check: L4×4×¼, Lb = 28 in,
  Cb = 1, cold: Ma = 23.4 kip·in (test_dome_steel.py).
- Section properties: AISC Shapes Database v16.0 (`kiln-hardware.md` §4.7.1 [S28]).
- Not used: AISC §D2 tension and §J3 threaded parts (not read; `door-headers.md` notes this). The
  rods keep HarbisonWalker's 12,000 psi on the tensile stress area (`kiln-hardware.md` §4.3).
- Eurocode 3 EN 1993-1-2 Table 3.1 was **not read** for this note, so its factors are not used;
  AISC's Appendix 4 table is.

## S3. Hot steel (Verified in `door-headers.md` §D6 [H7] [H23])

- AISC 360-16 Table A-4.2.1, ky = Fy(T)/Fy: 68–600 °F "use ambient properties"; 750 °F 1.00;
  800 0.94; 1,000 0.66; 1,200 0.35; 1,400 0.16; 1,600 0.07; 1,800 0.04; 2,000 0.02; 2,200 0.00.
  kE = E(T)/E: 200 °F 1.00; 400 0.90; 600 0.78; 750 0.70; 800 0.67; 1,000 0.49; 1,200 0.22;
  1,400 0.11. The engine interpolates linearly between rows (Derived).
- The table is for fire, a short event. Giles keeps carbon steel at or under 600 °F in continuous
  service in refractory concrete [H23].
- **The engine's rule (Derived):** the steel's temperature is the bearing walls' outside face from
  the engine's own steady wall solve at the top temperature (`heatloss.py`;
  `electric-and-thermal.md` §6). Past 1,400 °F, where the kE column ends, it refuses (no sourced
  stiffness). Past 600 °F it warns (Giles). Between, Fy and E are reduced by the table in F10.
  A hot gas leak at a door seal is outside this model (Olsen p.175 on seals and warped frames).

## S4. The dome's buttress angle and ties (Derived)

The dome's thrust on the walls comes from the sliced-dome analysis already in the engine
(`domes-over-doors.md` §D4, Heyman's half-dome slicing and the safe theorem; the heated factor of
`arch-thrust-theory.md`): with a whole-wall door the slices span the two walls either side of
it, and the door wall and the wall opposite carry nothing. On each bearing wall:

1. An angle along the top of the wall, at the springline, bends between posts as a simple beam
   under the **peak** hot slice thrust H taken along the whole bay: M = Hℓ²/8. This is cautious:
   H falls toward the end walls.
2. It must hold M ≤ M_a = M_n/Ω_b by AISC F10 (unbraced over the bay, toe in compression, Cb = 1,
   the cautious case), at the steel's temperature, **and** M/S_x ≤ 12,000 psi (HarbisonWalker's
   limit for bindings that may run hot, as the sprung-arch frame uses).
3. Posts: corner posts, and more along the sides (tied over the crown) if no listed angle and rod
   carry the bay, as for a sprung arch (`frame.py`, `_posts_per_side`).
4. Rods tie each pair of posts across; the end pair runs across the door's head and across the
   back wall (`domes-over-doors.md` §D4.1 step 4). Busiest rod: P = Hℓm, m = ½ with corner posts
   alone; checked at 12,000 psi on the tensile stress area.
5. The same angle runs round the springline across the door's head and the back, as a ring
   (the "metal tension ring" of [D3], the bands of Bourry and Searle).

Membrane theory (Timoshenko, `domes-over-doors.md` §D1–D2) gives a lower four-wall thrust, but
only with no door in a wall the dome bears on. With a whole-wall door the sliced state is the one
sourced, and it is used consistently here.

## S5. A door *below* the springline in a wall the dome bears on (a lintel)

The engine's door is a whole wall: the dome is sliced so that nothing bears on the door wall, and
the angle across the door's head is a tie and frame member, not a lintel. A smaller door opening
inside a bearing wall is not modelled. For it, the sourced method would be:
- a steel lintel carrying the masonry above the opening as **load only** (BIA TN 31B: with no
  arching assumed, the full weight of masonry and superimposed loads above the opening;
  `door-headers.md` §D1.1) plus the dome's vertical edge load over the opening (the slice V of
  §D4.1), checked by AISC F10 hot as in §S4; deflection L/600 (BIA, MSJC);
- and the dome's thrust over the opening carried by the frame (§S4), since a wall with a hole in
  it cannot buttress it.
No refractory allowable stress is needed for that route, because the steel carries everything
above the opening. The bearing of the lintel's ends on refractory masonry still needs an
allowable bearing stress, which is **NOT FOUND** (`door-headers.md` §D8), so that route would
still have to report its end bearing as unchecked. Implemented 2026-10-30 (`door.py`, sheet
`frame.door-lintel`) for a door in part of a wall (`loading.opening`, head `lintel`): the span is
the clear width plus TMS's 4 in bearing, the least angle BIA's 3½ in leg ¼ in thick, the steel's
temperature the door wall's outside face, the roof's edge load the dome's heaviest slice's half
weight (cautious) or a round roof's weight spread round the wall; the ends' reactions are reported
and their bearing stress is left unchecked (`door-openings.md`). Olsen's built kilns arch their
doors instead (`door-openings.md`); the arched head is laid out but not checked.

## S6. Gaps

- Eurocode 3 Part 1-2 Table 3.1 (not read here).
- Allowable stress or creep of carbon steel held hot over many firings (ASME II-D not read).
- Measured steel temperatures at kiln door heads.
- Bearing stress of steel on IFB or hard firebrick.
- A studio dome kiln with a steel lintel over a door in a bearing wall, with sizes.
