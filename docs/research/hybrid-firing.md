# Hybrid firing: elements and burners together, burner sizing for firing time, fast firing

Research for the hybrid cross-draft kiln (about 45 ft³, cone 10, 11.5 kW of elements, 8 Ransome
B3 venturi burners, 452,000 BTU/hr, IFB walls, about 2,600 lb of ware and shelves). Questions:
can elements and burners run together; when must the elements be off; how big must the burners be
for an 8–12 h or a 4–6 h firing; can the propane supply keep up; and how fast can ware be fired.

Status words: **verified** (read from the source), **secondary** (search summary, forum, or a
source quoting another), **unverified**, **gap** (not found). Olsen = *The Kiln Book*, 4th ed.;
page numbers are only those already quoted in `kiln-reference.md` and `olsen-kilns.md`.

Read 2026-10-30.

---

## 1. Electric and gas heat together

### 1.1 Running both at once vs hand-over

- **No source found** that describes a studio gas/electric hybrid's firing practice (both on at
  once, or a hand-over temperature). `electric-and-thermal.md` §1.5 already records: "Guidance
  from Kanthal or kiln makers on elements in gas/electric hybrid kilns: not found." This search
  did not change that. **Gap.**
- A patent describes switching element heating off during high-temperature reduction, and says
  SiC elements are not harmed by reduction (`electric-and-thermal.md` §1.5, [S12] there).
  Secondary.
- Forum: a hybrid kiln was marketed as giving about three times normal element life; a commenter
  doubted it "especially if you're messing with reduction" [H3]. Anecdote, secondary.
- Olsen's notes list an electric kiln with a wood-smoke firebox (`electric-reduction-smoke`,
  p.250, `olsen-kilns.md`); the repo has no details of its firing. Hybrid practice from Olsen:
  **gap** (ask the user for p.250).
- Physics, no source needed beyond the engine's own models: heat inputs add. Element power is
  fixed by the wire (11.5 kW ≈ 39,200 BTU/hr, **derived** at 3,412 BTU/kWh); burner heat to the
  kiln is input × available heat, which falls with flue temperature (§2.3). So the elements are
  about 9 % of the 452,000 BTU/hr burner input, but a larger share of the *delivered* heat late in
  the firing, when available heat is low. **Derived.**

### 1.2 Elements in reduction

| Claim | Source | Status | Tag |
|---|---|---|---|
| FeCrAl elements are protected by an Al₂O₃ layer; life "is determined by the rate at which the Aluminum oxidizes" | Skutt, *Top 5 Ways to Extend the Life of your Kiln Elements* | verified | [H1] |
| "Trying to reduce in your kiln will clobber their useful life and is definitely not recommended." | Skutt [H1] | verified | [H1] |
| Max element temperature, Kanthal A-1/APM: 1400 °C dry air (APM 1425); 1150 °C exothermic gas (10 % CO, 15 % H₂); **1050 °C endothermic gas (20 % CO, 40 % H₂)**; D 1000 °C | Kanthal handbook table, `electric-and-thermal.md` §1.4 [S9] | verified | |
| Pre-oxidise 7–10 h in air at 1050 °C before use in protective atmospheres | Kanthal, `electric-and-thermal.md` §1.5 [S9] | verified | |
| Reducing atmospheres corrode the oxide crust; re-oxidising firings advised after reduction | `electric-and-thermal.md` §1.5 [S10] [S11] | secondary | |
| A technical document on electric kilns in reducing conditions says definite figures for Kanthal element life in such atmospheres "cannot be given" | search summary of BC archive text [H4] | secondary | [H4] |
| Fire in oxidation to about 900 °C before reducing | Finkelnburg, *Ceramics Monthly* 2022, `combustion-and-masonry.md` §8 [S66]; used as `hybrid.REDUCTION_START` | secondary (1 source) | |

**What the engine can use.** The 1050 °C limit is a Kanthal *element* temperature in a defined
CO/H₂ gas, not a kiln-reduction limit; kiln reduction gas composition differs. The ~900 °C
reduction start is from one source. No source gives element life (firings) versus reduction
exposure. "Elements off at reduction start" is the conservative reading of [H1] and [S9]; it is
**not** a sourced hand-over rule. The task's 1650 °F (≈ 900 °C, cone 012–010) matches
`REDUCTION_START`. Note: the element wire runs hotter than the kiln, so it reaches 1050 °C before
the kiln does (the margin is in the surface-load data, `electric-and-thermal.md` §1.6).

---

## 2. Burner sizing: heat-up rate vs steady loss

Pointers; the data is already in the repo.

- **Olsen Rule 1** (p.226, `combustion-and-masonry.md` §3.1): IFB kiln about 10,000 BTU/ft³/hr
  at peak; dense brick 16,000–19,000. Most gas kilns overpowered. Verified (from the book).
- **Olsen's slower kiln** (p.226 context, `olsen-kilns.md` line ~254): a 36 ft³ dense-brick
  cross-draft with six venturis at 36,000 BTU/hr each, fired in about 12–15 h; 6,000 BTU/ft³/hr
  **derived**, well under his own dense-brick figure. Shows firing time stretches rather than
  failing when input is low.
- **Ward Data Guide** (`combustion-and-masonry.md` §3.1, `data/gas.yaml`) [S28] [S29]:

  | Wall | Cone 10 BTU/ft³/hr |
  |---|---|
  | 9 in hard brick | 16,000–20,000 |
  | 9 in IFB | 10,000–16,000 |
  | 6 in fibre | 7,000–10,000 (1996 article: 7,000–11,000) |

  "The high end of each range gives about a 6 to 7 hour firing (the article says 6 to 8 hours).
  The low end gives about 14 to 18 hours." Ward calls the table "a guide, not a guarantee".
  Single primary author. Secondary.
- Kiln listings bracketing Ward: Laguna LE-2040 ≈ 10,000, NM Clay ≈ 24,000 BTU/ft³/hr (derived)
  [S85 in combustion-and-masonry.md].
- **Author's kiln**: 452,000 / 45 ≈ 10,000 BTU/ft³/hr (**derived**) is the low end of Ward's IFB
  cone 10 range, which Ward ties to 14–18 h, not 8–12 h. By Ward's table, 6–8 h needs the high
  end, 16,000 BTU/ft³/hr ≈ 720,000 BTU/hr (**derived**). Ward's table carries no ware-load term;
  the 2,600 lb load is heavier than any source states. **Gap:** no source ties BTU/ft³/hr to
  load mass.
- **Heat-up vs steady loss.** No source splits burner input into "storage" (walls, ware) and
  "loss" (walls, flue). The engine's simulation does that from first principles. **Gap** for a
  sourced rule.
- **Available heat vs flue temperature**: `combustion.py` computes it with Cantera 3.2 and
  GRI-Mech 3.0, propane HHV 21,548 BTU/lb, 91,502 BTU/gal (`combustion-and-masonry.md` §1.1
  [S1] [S2]). Its docstring: available heat "falls steeply as the kiln gets hotter, and that is why
  a gas kiln uses most of its fuel near the top." Use that, not a table.

---

## 3. Fast-fire practice

| Kiln | Time to cone 10 | Lining | Input | Source | Status |
|---|---|---|---|---|---|
| Olsen fast-fire wood kiln, 12–16 ft³ | 3½ h (p.139); log 4 h 45 min "slow" (p.309); 1 h 55 min at 6000 ft | 4½ in 2300 °F IFB, one brick thick (p.140) | wood, < ¼ cord for 3½–4 h (p.143); BTU/hr not given | `olsen-kilns.md` §4 | verified (book) |
| All-hard-brick 40 ft³ version | averages 12–14 h | hard brick | not given | Olsen p.143 | verified (book) |
| Olsen 24 updraft gas kiln | 8 h, some glazes 4 h | not in the notes | not in the notes | Olsen p.139, `olsen-kilns.md` line 185 | verified (book) |
| Olsen Fast Fire (articles) | 6–8 h (another says 8–12 h) | — | "less than half a cord" | [S48] in combustion-and-masonry.md | unverified |
| Ward, high end of each range | 6–8 h | 9 in IFB: 16,000; fibre: 10,000–11,000 BTU/ft³/hr | | [S28] [S29] | secondary |

- **Fast-fire BTU/ft³/hr from a source: only Ward's high-end figures** (IFB 16,000 for 6–8 h).
  No source gives BTU/ft³/hr for a 4–6 h gas firing to cone 10. **Gap.**
- Olsen's fast kilns are small (12–16 ft³), thin-walled IFB, and lightly loaded; his 40 ft³
  hard-brick kiln takes 12–14 h. Nothing in the repo notes shows a 45 ft³ kiln with a
  2,600 lb load fired in 4–6 h. **Gap.**

---

## 4. Propane supply for a higher draw

Already in `combustion-and-masonry.md` §2 and `data/gas.yaml`:

- 100 lb cylinder, full, at 40 °F: 214,000 BTU/hr optimistic (§2.1 [S3]); 25 % full, ≥ 10 psi:
  61,500 BTU/hr conservative (§2.2 [S11]). The tables disagree a lot.
- ASME tanks: D × L × K (§2.3); ⅓-full table (§2.4), e.g. 500 gal 757,300 BTU/hr at 40 °F.
- Ward: 40 ft³ soft-brick kiln wants a 250 gal (summer) or 500 gal tank (§2.5 [S20]).
- Manifolds: Ward sells 2- and 3-tank connectors to "help prevent tank freeze up" [S24]; that
  capacities add in parallel is an **inference, not sourced** (§2.6). Never heat a tank [S23].
- Regulator margin: RegO 597F rated at 20 % droop with inlet 20 psig over set (§2.8 [S89]).
- **Derived** for 452,000 BTU/hr at 40 °F: about 8 cylinders on the conservative table, about
  3 on the optimistic one; at 720,000 BTU/hr, proportionally more, or a 500 gal tank.
- Vaporizers and liquid-withdrawal systems for large draws: **not searched to a readable source.
  Gap.**

---

## 5. Limits of fast firing on ware

### 5.1 What a 4 h cone 10 implies (derived)

Cone 10 ≈ 1285 °C (cones.md, 60 °C/h column). From 25 °C, 1260 °C in 4 h ≈ 315 °C/h average.
With the last 100 °C at Orton's 60 °C/h (1.67 h), the remaining ≈ 1,160 °C must rise in 2.33 h
≈ 500 °C/h. At Orton's 150 °C/h final rate (0.67 h), the rest is ≈ 350 °C/h. **Derived.**

### 5.2 Sourced rates

| Item | Value | Source | Status | Tag |
|---|---|---|---|---|
| Orton final rates for cone tables | 60 and 150 °C/h (last ~100 °C) | `cones.md`, `cones.yaml` | verified | |
| Bartlett Fast Glaze cone 6 (controller program) | 316 °C/h (570 °F/h) to 1083 °C, then 111 °C/h (200 °F/h) to 1222 °C; no hold | Digitalfire schedule BRTF6 | verified | [H2] |
| Bisque, thin even ware | "up to 500F/hr should be fine" | Digitalfire (search summary) | secondary | [H5] |
| Quartz inversion, porcelain | slow through about 900–1200 °F; one example 50 °F/h through 950–1150 °F; lustre cone 10 porcelain "super slow (e.g. 25 degrees per hour)" | Digitalfire (search summary) | secondary | [H5] |
| Firing speed vs evenness | "the speed of firing is not the determining factor, the key is the avoidance of uneven distribution of temperature across the piece" | Digitalfire (search summary) | secondary | [H5] |
| Cristobalite range | 210–280 °C (another Digitalfire page 100–270 °C) | `castables-minerals.md` [S24] [M5] | secondary | |
| Forum: kilns may not hold 300 °F/h near the top of cone 10 | community.ceramicartsdaily.org | secondary | [H6] |

- **No sourced maximum heating rate for ware was found.** Digitalfire frames the limit as
  temperature evenness across the piece (thickness, cross-section), not a single rate. The
  fastest sourced glaze schedule is 316 °C/h to ~1083 °C (cone 6, electric, [H2]); the 4 h
  cone 10 needs ~350–500 °C/h, faster than any sourced schedule. **Gap.**
- Water smoking / chemically bound water and carbon burnout rates: not sourced here (glaze firings
  of bisqued ware skip most of it). **Gap.**
- Dunting is mainly a cooling problem; not researched here. The engine models heating.

---

## 6. Gaps

1. Any studio hybrid kiln practice (both on together, hand-over temperature). Olsen p.250 not read.
2. Element life (number of firings) versus reduction exposure; a kiln-specific, not
   Kanthal-gas, reduction temperature limit. Reduction start 900 °C has one source [S66].
3. A sourced split of burner input into heat-up and steady loss; BTU/ft³/hr versus load mass.
4. BTU/ft³/hr for a 4–6 h gas firing to cone 10; any 45 ft³ heavily loaded fast firing.
5. Vaporizer / liquid-withdrawal capacity data; NFPA 58 manifolding rules.
6. A sourced maximum heating rate for ware; a fast cone 10 schedule (Orton/Bartlett);
   water-smoking and burnout rate limits.

---

## Sources

- [H1] Skutt, "Top 5 Ways to Extend the Life of your Kiln Elements". https://skutt.com/?p=12208
- [H2] Digitalfire, "BRTF6 – Bartlett Fast Glaze Cone 6". https://digitalfire.com/schedule/brtf6
- [H3] Ceramic Arts Network community, "Electric kiln manufacturers: which are best", p.2.
  https://community.ceramicartsdaily.org/topic/13498-electric-kiln-manufacturers-which-are-best-and-what-to-look-for/page/2/
  (search summary)
- [H4] BC archive extracted text on electric kilns in reducing conditions.
  https://bchdp.arcabc.ca/_flysystem/repo-service/2025-06/98117-Extracted%20Text.txt (search summary)
- [H5] Digitalfire pictures/pages on quartz inversion and bisque rates.
  https://digitalfire.com/picture/3471 ; https://digitalfire.com/picture/2436 (search summary)
- [H6] Ceramic Arts Network community, "Cone 10 glaze firing schedule for an electric kiln".
  https://community.ceramicartsdaily.org/topic/20654-cone-10-glaze-firing-schedule-for-an-electric-kiln/
  (search summary)
- Others by their tags in `electric-and-thermal.md`, `combustion-and-masonry.md`, `cones.md`,
  `castables-minerals.md` and `olsen-kilns.md`.
