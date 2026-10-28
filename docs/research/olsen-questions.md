# Olsen questions: springs, frames, arch thickness, chimney

Short pass, 2026-10-24. These are things the user could not quickly find in Olsen's *The Kiln Book*.
The material already in `kiln-hardware.md`, `combustion-and-masonry.md` and
`arch-thrust-theory.md` is not repeated here; this file points to it. Statuses:
**Verified** means the text was read on the page. **Excerpt** means only a search-result snippet
or summary was seen. **Not found** means no source turned up.

## 1. Springs on tie rods

| Item | Finding | Status | Source |
|---|---|---|---|
| Olsen's valve springs | No page found that quotes Olsen on springs, a spring type, wire size, free length, load or preload. | Not found | – |
| Why springs (historic) | A strong spring between the plate and the tie-rod nut keeps the arch pressure steady while the rods and the masonry expand and contract, so the arch does not lose support. | Excerpt | [O1] |
| Kiln patent | The springs sit outside the insulation. Nuts set how far they are compressed, which sets the prestress. | Excerpt | [O2] |
| Industrial practice | Springs take up a set amount of expansion, and the nuts are loosened gradually as the battery heats. | Excerpt (already in `thermal-properties.md` [T21]) | [O3] |
| Against springs | CAD forum: one builder found that springs "get pushed out and don't return"; another said the angle-iron frame does the holding. | Excerpt (page returned 403) | [O4] |
| Existing repo data | The Durango kiln used ½ in rod with springs. HarbisonWalker says "in some cases" spring-loaded. Pitelka advises against springs. | Verified | `kiln-hardware.md` [S17] [S20] [S11] |

None of these sources gives a spring rate, preload or expected arch growth. **Ask the user for
Olsen's pages.**

## 2. Frame members

| Item | Finding | Status | Source |
|---|---|---|---|
| Layout | Angle at each corner, joined along the bottom and across the sides about halfway up. Angle runs behind the skewbacks, with all-thread across the top so it can be tightened. No sizes given. | Excerpt | [O4] |
| Sizes | Already in the repo: Rhodes says 2×2 in angle for small kilns and channel buckstays for large ones. Durango used 3 in angle and 6 in channel. | Verified / Excerpt | `kiln-hardware.md` [S34] [S17] |
| Size against span table | None found. | Not found | – |

## 3. Arch thickness against span

| Item | Finding | Status | Source |
|---|---|---|---|
| 4½ in arch with fibre over it | One builder's plan on a forum (anecdote, not a rule) | Excerpt | [O5] |
| General masonry | Segmental rise/span ratio 0.15 to 0.5. A semicircular arch can be as shallow as ½ a brick length (veneer brick, not a kiln). | Excerpt | [O6] |
| Brick or castable thickness against span rule | None found. The thickness limit from thrust theory is in `kiln-hardware.md` §4.3. | Not found | – |
| Lifting, settling, rod adjustment in firing | Industrial practice loosens the nuts during heat-up [O3]. Other reports are in `thermal-properties.md` §2.3. | Excerpt | [O3] |

## 4. Chimney and flue

| Item | Finding | Status | Source |
|---|---|---|---|
| Height rule | Olsen: 3 ft per ft of downward pull plus 1 ft per 3 ft of horizontal run, measured from the **crown** (Cardew measures from the springer). | Verified (secondary) | `combustion-and-masonry.md` [S82] [S37] |
| Inlet and outlet area | In Olsen's downdraft designs the inlet area equals the outlet area (forum, secondary) | Excerpt | [O7] = [S83] |
| Flue area per ft³ | No source quotes an Olsen figure. One forum poster says books oversize flues and that the ratios are not consistent between books. | Not found | [O8] |
| Page citation to Olsen | None found online. | Not found | – |

Independent sources in this pass: patents ×3, the CAD forum (two threads, counted as one), and one
masonry brief. No online text of Olsen was reached, and archive.org full-text search found
nothing.

## Sources

- [O1] US 15,832, "Improvement in furnaces" (1856). https://patents.google.com/patent/US15832
- [O2] US 4,512,738, "High-temperature kilns". https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4512738
- [O3] US 3,054,730A, coke oven anchoring. https://patents.google.com/patent/US3054730A/en
- [O4] CAD forum, "metal frame for sprung arch kiln". https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/
- [O5] permies.com, "Arch Top Bell flat". https://permies.com/mobile/t/218869/Arch-Top-Bell-flat
- [O6] BIA, Brick Brief: Arches (May 2012). https://www.gobrick.com/media/file/brick-brief-arches-may-2012.pdf
- [O7] CAD forum, "inlet height vs chimney height". https://community.ceramicartsdaily.org/topic/4294-inlet-height-vs-chimney-height/
- [O8] CAD forum, "chimney entrance reduction". https://community.ceramicartsdaily.org/topic/17145-chimney-entrance-reduction/
