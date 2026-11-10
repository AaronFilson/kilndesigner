# The fireboxes' air intakes: how they are sized, and each kiln's

Research A2 of the round of 2026-11-10 (`docs/planning/11-10-26.md`), for ADR 0017 decision 9:
"λ is worked out from the fireboxes' air intakes, sized from the reference material on them, and
from the draft." What the reference material says about sizing ash-pit mouths, primary and
secondary air and stoke holes, and each stoked kiln's intake areas, by the precedence of
`11-09-26.md` §A (printed > scaled with its spread > "(drawing)" > left out).

Olsen is *The Kiln Book*, 4th ed., by printed page; his rules are quoted from `kiln-reference.md`
§9, §12, §13 and §14 (read from the scan, **Read** there) and each kiln's facts from
`core/tests/v2/reference_kilns.yaml` (with their status). The open sources on hand-fired furnaces
are read in `grates-and-fuel-beds.md` (the same round) and summarised in §2. Marks: **Read**,
**Snippet**, **Derived** (arithmetic shown; `scratch/research-a/intakes.py`), "from memory".
Worked 2026-11-10.

## Short answer

- **The book gives no area rule for any air intake.** It sizes the grate and the firebox floor
  against the chimney (grate 10 × the chimney's section, now about 7 : 1, p.76–77; the firebox
  floor 10 × the chimney, the fast-fire's plus 20 %, p.140, p.199), the inlet flue against the
  chimney (inlet = exit = chimney section for natural draft, p.78), and gives the intakes as kinds
  and a few fixed sizes: air at three levels (ash pit, grate, stoke hole), each openable (p.180,
  p.200); mouse holes about 2½ in square running 12–15 in into the ash pit (p.204); a hob
  firebox's secondary-air holes 4½ × 4½ or 2½ × 9 in, clean-out holes 4½ × 4½ in (p.203–204); a
  5 in perforated clay tube spreading air under a grate (p.116, p.206); "the ash-pit entrance fully
  open" (pp.188–189). The stoker opens and closes them: Singh's coal kiln's fire mouth is open for
  hours 1–3 and bricked up from hour 4 (p.133, Table 5-1).
- **The open sources** on hand-fired furnaces (grates, air space, ash-pit doors) are research A3's
  (`grates-and-fuel-beds.md`); §2 summarises them.
- **Each kiln's intakes** (§3): printed or derived from printed sizes for 16 of the 38 stoked
  kilns; scaled for a few more; the rest print none (their gaps). Where both are printed, the
  intakes below the grate are 1.4–6 times the chimney's section and the stoke holes 0.3–2.2 times
  (Derived, §3): fully open, the openings below the grate are not the narrowest section of the gas
  path; the stoker's bricks and the fuel bed decide the air.
- **For the engine** (B4, §4): each intake as an opening of its printed (or scaled) area, sharp-
  edged, with the stoker's fraction open as the operating variable between closed and the printed
  maximum, and the fuel bed's resistance in series below the grate. λ then follows from the draft.

## 1. What the book says about the intakes (Read, as cited)

| Rule | Page | What it fixes |
|---|---|---|
| Grate area for natural draft: wood 10 × the chimney's section at its base; he now uses about 7 : 1; groundhogs about 4 : 1; a side stoke's area counts as grate; round up to brick sizes | pp.76–77, Figs 3-8 to 3-10 | the grate against the chimney |
| Coal grate: 1 ft² per 6–8 ft² of floor; four fireboxes 8 : 1, two 6 : 1; "too large a ratio is better than too small" | p.76, pp.206–207 | the coal grate against the floor |
| Oil combustion area 1 ft² per 5 ft² of floor, less with forced air | p.76, p.213 | the oil firebox |
| Firebox floor at least 10 × the chimney's section; the fast-fire's 10 × plus 20 % | p.199, p.140 | the firebox against the chimney |
| Natural draft: inlet flue = exit flue = chimney section | p.78 | the flues |
| What a wood firebox must do: preheat the air, let it rise through the grate into a secondary combustion space, leave room above the grate, give access for raking, have sized and spaced flue holes | p.199 | – |
| Air at three levels: plenty at ash-pit level and at stoking level, plus grate-level air round the grate's perimeter through mouse holes | p.200 | the kinds of intake |
| Mouse hole: a covered channel about 2½ in square, 12–15 in into the ash pit; feeds air to the coal bed, keeps the coal height down | p.204 | one size |
| Hob firebox (Fig 8-12): ash pits 18 in wide each side of a 4½ in hob; clean-out holes 4½ × 4½ in; secondary-air holes 4½ × 4½ or 2½ × 9 in; a 2½ × 2½ in mouse hole; primary air from the top | pp.203–204 | sizes for one firebox type |
| Multi-directional fireboxes: the design factors include "air at the ash pit, the grate, the firebox-floor level and the stoke hole, and the entrance width and height"; air below the grate, at the grate and at the stoke hole, each openable, built into the bricked-up door (Fig 7-4) | pp.179–180 | the kinds, adjustable |
| In practice: grate bars ¾ in apart; air holes in the door at grate level; "the ash-pit entrance fully open"; a 9 × 13 in stoke hole in each firebox door | pp.188–189 | one kiln's settings |
| Spreading the air: a 5 in extruded clay tube (square, p.206) with perforated sides under the grate, holes smaller at the supply end, a shutter outside | p.116, p.206 | a distributor, not an area |
| A better chamber firebox: more, smaller air holes spread evenly; grate bars at minimum spacing; grate-level mouse holes that can be opened | p.202 | a direction, not an area |
| Ash too close to the grate chokes the air; coals built up to the bars choke the kiln ("the kiln will literally stop"); rake the ash pit | p.194, p.117 | the bed's resistance, qualitatively |
| The ash pit preheats the combustion air ("free-breathing grate") | p.168 | – |
| Air preheat: every 400 °F of air preheat adds about 100 °F to the flame | p.199 | – |
| Gas: secondary air through the burner ports; its control matters for atmosphere | p.173, p.235 | burner kilns |
| Drip oil: at most one port per 9 in of inlet-flue wall, at least one per 18 in | p.208 | the oil drip's ports |
| Fast-fire firing: "beat the wood down on the grate for more oxygen"; rake and clear coals if the kiln loses temperature; never let the coals under the grate build up to touch it | p.143 | the bed |
| Singh's coal kiln: fire mouth open hours 1–3, bricked up hours 4–6 and on | p.133, Table 5-1 | a printed intake schedule |

A secondary source the repo already holds: King and Harrison's Bourry-box proportions, relative to
the chamber's floor area (exit flues 7.6–11.1, chimney 7–8.3, bag-wall opening 14.2–17, throat
arch 25–56.5), and a builder's fast-fire with a 13.5 in² primary inlet against an 81 in² firebox
port (`combustion-and-masonry.md` §5.2, secondary).

## 2. The open sources on air openings

Not yet integrated: research A3's `grates-and-fuel-beds.md` reads the hand-fired furnace literature
(grate air space, ash-pit doors, over-fire air); its findings on openings are summarised here when
it is committed.

## 3. Each stoked kiln's intakes

Areas are Derived from the printed (or scaled) sizes; "both" means the opening admits fuel and air
together. Statuses as the dataset's. The chimney's section is given where printed, for scale.

| Kiln | Below the grate (primary) | Above the grate: stoke hole and air holes | Area, in² (Derived) | Chimney section | Status and notes |
|---|---|---|---|---|---|
| `anagama-hole` | no grate | entrance and firebox 2 × 2 ft (both) | 576 | 4½–7 in wide (scaled) | printed p.84; scales 15–23 × 29–45 in (oval) |
| `bae-gilgama` | no grate | a round-headed mouth, not sized | – | – | drawing Fig 4-69 |
| `bidai` | Fig 8-7's side view labels AIR over the 14 in ash pit, STOKING above it; the plan's front opening is 12–14 in wide | the stoking opening above; its height not legible; Fig 4-36's mouth 9 in wide | 168–196 below (12–14 × 14) | a grid of 9 × 9 in channels | printed p.201, read on the page image 2026-11-10; uncertain |
| `blakebrough-sturt` | the channel's bottom, not sized | side stoke hole 10–15 in high | – | – | scaled (width foreshortened) |
| `breda-bottle` | ash pit 2 ft wide × 3½ ft deep | not sized | (1,008 if that is its mouth) | the bottle, 12 ft across at its base | printed Fig 6-50; whether 2 × 3½ ft is the pit's mouth isn't said |
| `chappell-domura` | not sized | not sized | – | 12 × 12 in tapering to 9 × 9 | – |
| `church-skaelskor` | ash pit and walkway 14 in wide × 18 in deep (Fig 7-3, the type's drawing) | not sized for this kiln (the Kanayama kiln's door stoke holes are 9 × 13 in, pp.188–189) | 252 each below | 13.5 × 13.5 in (the anagama chimney) | printed; two fireboxes |
| `conrad-teardrop` | ash pit 12 in deep, 24 in long; its mouth not sized | stoke hole 9 in high, width not printed | – | 9 × 9 in | printed p.124 |
| `ellington-new-hog` | an air hole 13½ in wide × 9 in high under each front stoke hole | three front stoke holes 13½ × 16 in; side holes about 4½ × 7½ in, two rows every 27 in | 364 below (three); 648 front stoke holes | not legible ("4'5" 3'") | printed Fig 4-97; side holes scaled |
| `falcone-pompeii` | a stoking port with an under-air supply | not sized | – | – | printed pp.160–161 |
| `fast-fire` | each firebox's mouth below the grate: 13½ in wide × 6–8 in (the grate 6–7 in up, p.199; its legs 7–8 in, p.204) | above the grate: 13½ × 4½–6½ in (the firebox 12½ in, five courses) | 162–216 below; 122–176 above (two fireboxes) | 9 × 9 in | derived from printed sizes (p.140, p.199, p.204, Fig 5-39); whether the mouth is partly closed in firing isn't printed |
| `fast-fire-anderson` | as the fast-fire (assumed) | as the fast-fire | 162–216; 122–176 | 9 × 9 in (assumed) | the design's assumption |
| `fireworks-edmonton` | ash pit 14 × 18 in (Fig 7-3); air below the grate, at the grate and at the stoke hole in the door, not sized (Fig 7-4) | not sized | 252 each below | split groundhog chimney; single anagama chimney | printed |
| `fujiwara-bizen` | no grate (the dogi's floor) | fire-mouth hole 3½ × 2 ft when open; side holes (takiguchi) about 5 in round | 1,008; 20 each side hole | round, entered through a 10 in hole | printed p.102; takiguchi scaled |
| `groundhog-basic` | not sized | not sized (Fig 3-10's 9 × 60 in side stoke counted as grate, p.77) | – | the kiln's width, 9–30 in | – |
| `hollyweird` | air holes at grate level, not sized; a 5 in tube under the second grate | stoke hole 9 × 13½ in in the door bricking | 122 | 15 × 24 in | printed p.117, p.116 |
| `hotchkiss-raw-clay` | not sized | stoke holes in both side walls, not sized | – | – | – |
| `kannofen` | two arched mouths (photo) | not sized | – | – | drawing |
| `kawaii` | as the Bidai kiln's dogi (p.97, p.200) | two extra stoke holes on the dogi's sides, not sized | – | – | – |
| `kenzan-muffle` | iron grate opening 15 × 19 in | not sized | – | – | printed Fig 6-47 |
| `kitade-tojilo` | two "air draft & ash pit holes" 12 in wide × 18 in tall | stoke hole 9 × 7 in | 432 below; 63 above | – | printed Fig 8-11 |
| `kyoto-climbing` | – | stoked through the takaguchi, not sized | – | – | – |
| `la-borne` | under a brick grate, not sized | not sized | – | – | – |
| `meaders-cheever`, `meaders-david` | no grate | not sized | – | 9 in × 5 ft; 9 in inside | – |
| `miravet` | no grate (fire chamber and ash pit in one) | firebox mouth 27 in high × 18 in wide, sill 3 ft up | 486 | a 15 in main flue in the dome | printed Fig 6-19 |
| `moveros-umbrella` | under the umbrella floor | firebox mouth 27 × 22 in | 594 | open top | printed Fig 6-3 |
| `ninodaguia` | – | firebox mouth 27 × 18 in | 486 | – | printed Figs 6-14 |
| `olsen-two-chamber` | first firebox: air along the front wall, the primary air while the space under the stoke hole is closed (p.202); second: a 5 in square perforated tube under the grate | second firebox stoke hole 7 × 7 in | 49 | – | printed |
| `phoenix-nh`, `phoenix-wright` | not sized | not sized | – | 9 × 9 in (assumed) | – |
| `singh-lowfire` | the pit's entry, 12–16½ in wide | not sized | – | – | scaled |
| `suzuki-kyoto`, `tobe` | – | stoke bays, not sized | – | – | drawing |
| `tamba` | – | side stoke holes about 7–7¼ in round | 38–41 each | – | scaled Fig 4-16 |
| `kato-coal` | ash pit 27 in deep (scaled, or 15 in) | fireboxes 2 ft 6 in wide at the outer mouth | – | round, 3 ft at the base | printed and scaled; the mouth's height not printed |
| `singh-coal` | "AIR SOURCE AND COAL ASH PIT 36" X 24"" at each of four fireboxes | stoke hole 15 × 13 in each | 3,456 below; 780 above (four) | 24 × 24 in | printed Fig 5-11; the fire mouth open hours 1–3, then bricked up (Table 5-1) |
| `olsen-oil-drip` | – | three drip ports, each about 7½ in wide × 24 in high, open to the air | about 180 each | – | scaled Fig 8-20 |

Against the chimney, where both are printed (Derived): the fast-fire's mouths below the grate are
2.0–2.7 × its 81 in² chimney and above it 1.5–2.2 ×; the Church kiln's ash pits 1.4–2.8 × (one or
both fireboxes); Singh's ash pits 6.0 × and stoke holes 1.4 ×; Hollyweird's stoke hole 0.3 × (its
grate-level air holes not sized); the Bidai air opening 2.1–2.4 × one 9 × 9 in channel of its
chimney grid.

## 4. For the engine (proposed, B4)

- Each intake an opening of its printed or scaled area, below or above the grate, sharp-edged (the
  loss coefficients of `fittings-and-kiln-convection.md`), in the draft's pressure balance; the
  stoker's fraction open is the operating variable, from closed to the printed size.
- Below the grate the fuel bed's resistance in series (`grates-and-fuel-beds.md`).
- λ through the firing is then the air these openings pass at the draft, against the fuel the
  stoker adds; reduction is the stoker's closing them (Singh's bricked-up mouth).
- Kilns with no printed intake: the opening is the design file's assumption, said so in the
  working, as the dataset's gaps list it.

## 5. Questions for the owner

1. **The fast-fire's firebox mouths**: the book prints the firebox (13½ in wide, 12½ in tall) and
   the grate's height (6–7 in, on legs 7–8 in), not whether the mouth is partly bricked in firing.
   Fully open, the mouths below the grate are 2–2.7 times the chimney's section. Were they open?
2. **Breda's 2 × 3½ ft ash pit** (Fig 6-50): its mouth, or its section?
