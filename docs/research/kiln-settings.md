# The reference kilns' settings: mass and envelope as sourced bands

Research for part C2 of the round of 2026-11-10 (`docs/planning/11-10-26.md` §C), for ADR 0017
decision 11: "The ware load is required. No heat result without a load in the design." The book
prints few loads, so each reference kiln's setting (ware and kiln furniture) is carried as a band:
its mass, from what is printed first and published figures otherwise, and its envelope, the
stacking space the book's own clearances leave in the chamber as v2 traces it.

Olsen is *The Kiln Book*, 4th ed., cited by its printed page. Marks as in the other research files:
**Read** (on the page or the source), **Derived** (arithmetic, shown), **Assumed** (a stated band
where no source gives the value). Worked 2026-11-10; the module is `core/tests/v2/loads.py`, the
bands are the dataset's `setting` facts (`core/tests/v2/reference_kilns.yaml`), the arithmetic
`scratch/c2/settings.py` (git-ignored).

## Short answer

- **Mass of each chamber's setting** = ware + shelves:
  - ware **60–260 kg per m³ of the chamber's fired volume** (the EU BREF's "setting density" of
    periodic and tunnel kilns firing whiteware and technical ceramics, §2); a kiln maker's test
    loads, 100 lb in a 10 ft³ kiln, 160 kg/m³, fall inside;
  - shelves: **one layer** (the setter shelf, p.172) **to one layer every 6¾ in** of the setting's
    height (a kiln maker's furniture kit: four layers in a 27 in kiln, §3), each covering the
    setting's plan at **8–22 lb per 12 × 24 in shelf** (Olsen pp.33–35: Advancer to silicon carbide);
    posts left out (no source sizes them; §3).
- **Printed figures first**: Falcone's 20 short tons of bricks and tiles (p.160); the fast-fire's
  12 × 24 × 1 in shelves (p.139) and plan (p.142); Kähler's 24 × 24 in stacking to the arch line
  (p.136); Blakebrough's two 24 × 24 in shelves (p.148); Kaneko's 9 in combustion width (p.172);
  Singh's 12 in round the saggars and 6–8 in under the dome (p.135); Kato's 1 ft under the crown
  (p.131); Fujiwara's 6 in under the roof (pp.102–103); Kyoto's 9 in at the front wall (p.93,
  p.205); Tamba's pots set without shelves (pp.85–86).
- **The envelope**: the room inset by the combustion space, 4½ in (p.171; 6 in the band's other
  end, for a 4 in tip), from 2½ in up (p.172), to the springline in an updraft (p.74) or the roof
  less the same space elsewhere; on a curved wall or under a low arch the largest such box that
  fits (§4).
- **The fast-fire's survey load, 55 kg** (three 12 × 24 × 1 in shelves, posts and about 25 kg of
  ware; `thermal-combinations.md` §4.1), lies inside its band, **40–159 kg**, at 13 % of the way
  from the light end: a light setting by these sources. Its tests keep the 55 kg.
- **The setting's emissivity**: 0.52–0.77, nominal 0.75 (§6).

## 1. What the book prints (the dataset's `setting` and `ware` facts)

| Kiln | Printed | Page |
|---|---|---|
| fast-fire | 12 × 24 × 1 in shelves; 4½ in clear each side and in front, 1 in at the back; the bag walls' two rowlock rows carry the first shelf | p.139, p.142, Figs 5-35, 5-43 |
| kahler-salt | 16 ft³ of stacking, 24 × 24 in between the dashed lines (3 in a side, 6 in at each end), to the arch line | p.136, Figs 5-17, 5-18 |
| blakebrough-tasmania | two 24 × 24 in shelves raised off the floor, a 9 in burner channel along each side; "a 40 cu. ft stacking" kiln | p.148 |
| kaneko-car | a 9 in combustion width round the floor; 500 cu ft (probably stacking) | pp.170–172 |
| singh-coal | saggars stacked to within 6–8 in of the dome, about 12 in clear round them up to the skewbacks | p.135 |
| kato-coal | 1 ft from the top of the setting to the crown | p.131, Fig 5-4 |
| fujiwara-bizen | 6 in between the top setter and the roof; 3 × 5 in under-draft spaces | pp.102–103 |
| kyoto-climbing | a space at least 9 in wide between the setting and the front wall | p.93, p.205 |
| falcone-pompeii | 20 short tons (18 t printed beside) of bricks and tiles a cycle | p.160 |
| tamba | up to 500 pots 13–24 in tall, set without shelves on saggar setters | pp.85–86 |
| ninodaguia | 2000–3000 small pots or about 1000 large ones, 8 or 9 high on setter tiles | pp.156–157 |
| hollyweird | 12 × 24 in shelves (one 12 × 18 in); pots in the flues between chambers | p.116, Fig 4-110 |
| hohr-2003 (extra) | 6 (?) 40 × 50 cm shelves | p.122 |
| olsen-chamber-p23 (extra) | fire tiles 12 × 18 × 2 in as shelves | p.23 |

No kiln's setting is weighed in the book except Falcone's (ware only). The counts of pots
(Tamba, Niñodaguia) give no mass: no source weighs those pots.

## 2. Ware per volume of kiln (Read)

**EU BREF, Ceramic Manufacturing Industry** (European Commission JRC, August 2007; the copy read is
the Ukrainian ministry's mirror of `cer_bref_0807.pdf`, text extracted 2026-11-10). Its glossary
defines **setting density** as the "mass of the ware to be fired without firing auxiliaries in the
fired volume of the kiln in reference to the overall fired volume of the kiln": the ware alone,
over the whole fired volume, so it multiplies the chamber's volume, not the stacking space's.

| Kiln and ware | Setting density, kg/m³ | Where |
|---|---|---|
| Porcelain, tunnel kilns, biscuit and glost | 60–70 | Table 2.18 |
| Porcelain, fast-firing tunnel kilns | < 100 | Table 2.18 |
| Porcelain, a shuttle kiln: 0.91 t a cycle in 7.0 m³ | printed 12.8; 130 (Derived, 0.91 t ÷ 7.0 m³) | Table 2.17 |
| Sanitaryware, shuttle kilns: 5–15 t in 50–150 m³ | 100 | Table 2.23 |
| Sanitaryware, tunnel kilns | 100–150 | Table 2.22 |
| Electrical insulators, a 100 m³ shuttle kiln, to 1300 °C | 260 | §2.3.8 |
| Kiln furniture (H-cassettes), a 12 m³ shuttle kiln | < 300 | §2.3.8 |
| Vitrified clay pipes, tunnel kilns | 150–300 | Table 2.7 |
| Roof tiles, tunnel kilns | 200–400 | Table 2.2 |
| Facing bricks and pavers, tunnel kilns | 650–1500 | Table 2.2 |
| Fireclay bricks, shuttle kilns | 650–1000 | Table 2.12 |
| Hoffmann chamber kilns, bricks | > 300 | §2.3.1.5 |

The porcelain shuttle kiln's printed 12.8 disagrees with its own 0.91 t in 7.0 m³ (130): a
misprint, the derived figure used.

**Paragon Industries, "Kiln Firing Costs"** (J. S. Hohenshelt, 2009; read on artclayworld.com):
"kilns that are about 10 cubic feet ... The tests were conducted using digital kilns with about 100
pounds of ware": 160 kg/m³ of kiln (Derived). Skutt's firing-cost example takes "a load 100 lbs in
the kiln" for its KM1231 (its volume not given there; skutt.com FAQ, read 2026-11-10).

**The band for pots: 60–260 kg/m³** of the chamber (Assumed from the above): periodic and tunnel
kilns firing ware set on furniture, from the porcelain tunnel kilns' 60 to the electrical
insulators' 260; the sanitaryware, porcelain shuttle and Paragon figures inside it. Bricks and tiles
set on each other run far denser (650–1500), and are used only where the book prints the ware
(Falcone: 18,000–18,144 kg in v2's 28.7 m³ chamber is 630 kg/m³, inside the bricks' range).

**Not found**: a weighed setting of a studio stoneware kiln, wood or gas, in any open source
searched (Ceramics Monthly, Ceramic Arts Daily, kiln makers' pages, GTZ/UNIDO kiln manuals). The
owner's own hybrid kiln, "about 2,600 lb of ware and shelves" in about 45 ft³
(`hybrid-firing.md`), is 926 kg/m³ of ware and shelves (Derived), far above this band's top for
that size (about 550 kg): a question for the owner (§7).

## 3. Kiln furniture (Read)

**Shelves.** Olsen weighs 12 × 24 in shelves (pp.33–35; `furniture.py`, `kiln-reference.md`):
mullite 1 in 20.5 lb, conventional silicon carbide 1 in 22 lb, cordierite up to 21 lb, Advancer
(nitride-bonded SiC) 8 lb. Makers and dealers list the 12 × 24 × 5/16 in Advancer at 8 lb (Sheffield
Pottery) and 9 lb (Marjon Ceramics, Sounding Stone), a 12 × 24 × ¾ in silicon carbide shelf at 20 lb
(Sheffield), a semi-hollow CoreLite cordierite 12 × 24 × ⅝ in at 11.5–11.8 lb (The Ceramic Shop,
Sheffield). As mass per area of shelf (Derived): 8 lb → 19.5 kg/m², 22 lb → 53.7 kg/m²; the
fast-fire's printed 1 in shelves 20.5–22 lb → 49.8–53.7 kg/m².

**Layers.** No source states a setting's shelf spacing. A maker's furniture kit sets how many
layers a kiln of a given depth is sold with: Skutt's kit for its KM-1027 (23 × 23 in, 27 in deep,
7 ft³; skutt.com) holds eight half shelves and 36 posts, six each of 1–6 in (School Specialty, Dick
Blick and Chesapeake Ceramics listings, 2026-11-10): four layers in 27 in, one each 6¾ in
(Derived). The band: one layer (the setter shelf at least 2½ in off the floor, p.172) to one each
6¾ in of the setting's height. Tamba's pots are set without shelves (pp.85–86) and Falcone's bricks
and tiles on each other: no shelves for those two.

**Posts** are left out: no source here sizes them (Skutt lists only their heights, 1–12 in; three a
shelf, two shared by half shelves on a layer, skutt.com "Furniture Kits"). They are small beside
the shelves.

## 4. The envelope (Read, then Derived)

The book sizes a kiln by its stacking space and builds the chamber round it
(`kit-stacking-space.md`). Its clearances:
- **combustion space** between the setting and the walls: at least 4½ in for floor burners or
  2½–3 in tips, usually the length of the wall (p.76, p.171; Fig 6-63's "4½" around"); 6 in for a
  4 in tip (p.171), the band's other end (`loads.envelopes(wide=False)`);
- **under the setter shelf**: at least 2½ in (p.172);
- **the top**: an updraft's arch sits on the cube, its volume collecting the flue gas (p.74), so its
  setting stops at the springline; under a flat roof or an open top at the springline (the round
  open-topped updrafts: pots "piled to the top of the chamber, never past it", p.153) the same
  combustion space is kept below it; in a cross- or downdraft the setting reaches up under the
  roof, and the same space is kept from the roof at the setting's edges unless the kiln prints its
  own (Kato's 1 ft, Fujiwara's 6 in, Singh's 6–8 in).

**How the envelope is found** (`loads.envelopes`): the room v2 traces (`chamber.Room`) inset by the
clearances; the roof over the setting's corners and edges, each pushed out by the clearance, read
by vertical rays on the chamber's traced faces (trimesh on Embree, as `rays.py`); a point outside
the chamber's plan has no roof over it. On a round wall, a crossing, a dome or an arch springing
low, the plan is narrowed across, along or both (to 0.3 of the inset room, in steps of 0.05) to the
box of most volume that fits. The box then lies in the chamber's gas (`Chamber.holds`, checked by
the heat model). Not kept: a round chamber's stacking is a cylinder, the box its inscribed square
(about 64 % of the cylinder's plan). A tube cut into segments (`heat_model(segments=)`) keeps its
one band, shared by the segments' volumes, each part's box stopping ½ in short of a cut so the
boxes don't touch.

## 5. The bands, kiln by kiln (Derived; the dataset's `setting` facts)

Each chamber zone's band is the dataset's `setting` fact (kg), its reason the arithmetic. Rows of
chambers: one fact a chamber, each its own volume and envelope; the table gives the first
chamber's envelope and the whole kiln's sums.

| Kiln | Chambers | Chamber (m³) | Envelope (in) | From (in) | Ware (kg) | Shelves (kg) | Setting (kg) |
|---|---|---|---|---|---|---|---|
| anagama-hole | 1 | 4.58 | 40.5 × 117.0 × 23.0 | 2.5 | 275–1,192 | 60–493 | 335–1,684 |
| bae-gilgama | 1 | 2.77 | 33.1 × 63.0 × 34.6 | 2.5 | 166–719 | 26–362 | 192–1,081 |
| bidai | 3 | 8.56 | 64.0 × 29.7 × 39.2 each | 2.5 | 514–2,226 | 71–1,057 | 585–3,283 |
| blakebrough-sturt | 1 | 2.54 | 18.0 × 63.0 × 39.2 | 2.5 | 153–661 | 14–196 | 167–858 |
| blakebrough-tasmania | 1 | 1.93 | 24.0 × 48.0 × 45.0 | 2.5 | 116–502 | 15–239 | 130–742 |
| bowen-mountain | 1 | 1.08 | 27.0 × 38.2 × 18.7 | 2.5 | 65–282 | 13–72 | 78–353 |
| breda-bottle | 1 | 45.19 | 119.7 × 119.7 × 81.5 | 2.5 | 2,712–11,750 | 181–5,958 | 2,892–17,708 |
| chappell-domura | 1 | 1.42 | 27.0 × 51.0 × 29.0 | 2.5 | 85–369 | 17–191 | 102–560 |
| church-skaelskor | 1 | 6.69 | 75.0 × 60.0 × 40.3 | 2.5 | 402–1,740 | 57–780 | 458–2,520 |
| conrad-teardrop | 1 | 4.12 | 42.5 × 108.0 × 28.5 | 2.5 | 247–1,071 | 58–636 | 305–1,707 |
| electric-car-45 | 1 | 4.13 | 36.0 × 97.0 × 46.5 | 2.5 | 248–1,073 | 44–726 | 292–1,799 |
| ellington-new-hog | 1 | 10.50 | 49.9 × 93.1 × 17.7 | 2.5 | 630–2,729 | 59–322 | 688–3,052 |
| falcone-pompeii | 1 | 28.69 | 109.0 × 148.0 × 76.5 | 2.5 | 18,000–18,144 (printed) | none | 18,000–18,144 |
| fast-fire | 1 | 0.46 | 18.0 × 21.5 × 24.4 (printed plan) | 9.0 | 27–119 | 12–40 | 40–159 |
| fast-fire-anderson | 1 | 0.51 | 18.0 × 21.0 × 29.0 | 2.5 | 30–132 | 5–52 | 35–184 |
| fireworks-edmonton | 1 | 12.20 | 99.0 × 79.2 × 46.4 | 2.5 | 732–3,171 | 99–1,630 | 831–4,801 |
| fujiwara-bizen | 2 | 8.81 | 111.0 × 38.2 × 37.6 (first) | 2.5 | 529–2,291 | 85–1,082 | 614–3,372 |
| groundhog-basic | 1 | 6.83 | 55.8 × 135.0 × 20.5 | 2.5 | 410–1,777 | 95–783 | 505–2,560 |
| hollyweird | 2 | 9.52 | 46.0 × 87.0 × 29.2 (first) | 2.5 | 571–2,476 | 129–1,415 | 700–3,892 |
| hotchkiss-raw-clay | 6 | 23.54 | 51.0 × 45.9 × 47.2 each | 2.5 | 1,412–6,120 | 177–2,920 | 1,589–9,040 |
| kahler-salt | 1 | 0.89 | 24.0 × 24.0 × 45.5 (printed plan) | 2.5 | 54–233 | 7–120 | 61–352 |
| kaneko-car | 1 | 17.92 | 78.0 × 90.0 × 93.5 | 2.5 | 1,075–4,660 | 88–3,162 | 1,164–7,822 |
| kannofen | 1 | 7.33 | 32.3 × 168.2 × 51.2 | 2.5 | 440–1,907 | 69–1,319 | 509–3,226 |
| kato-coal | 1 | 7.48 | 58.6 × 75.0 × 44.0 | 2.5 | 449–1,944 | 55–914 | 504–2,858 |
| kawaii | 4 | 16.92 | 75.0 × 35.1 × 46.6 each | 2.5 | 1,015–4,399 | 133–2,189 | 1,148–6,588 |
| kenzan-muffle | 1 | 0.26 | 9.1 × 9.1 × 35.5 | 2.5 | 16–69 | 1–14 | 17–83 |
| kitade-tojilo | 1 | 4.14 | 35.1 × 87.0 × 38.6 | 2.5 | 249–1,077 | 38–529 | 287–1,606 |
| kyoto-climbing | 10 | 31.99 | 54.0 × 26.4 × 55.8 (first) | 2.5 | 1,919–8,316 | 206–4,533 | 2,125–12,850 |
| la-borne | 1 | 75.03 | 123.0 × 315.0 × 77.1 | 2.5 | 4,502–19,509 | 488–14,767 | 4,990–34,276 |
| meaders-cheever | 1 | 3.92 | 40.8 × 87.0 × 27.8 | 2.5 | 235–1,020 | 45–492 | 280–1,512 |
| meaders-david | 1 | 1.67 | 33.1 × 63.0 × 14.4 | 2.5 | 100–434 | 26–145 | 126–578 |
| miravet | 1 | 14.75 | 87.0 × 87.0 × 69.5 | 2.5 | 885–3,836 | 95–2,623 | 981–6,458 |
| moveros-umbrella | 1 | 2.22 | 35.7 × 35.7 × 41.0 | 2.5 | 133–578 | 16–265 | 149–843 |
| ninodaguia | 1 | 3.81 | 52.5 × 52.5 × 35.0 | 2.5 | 229–992 | 35–478 | 264–1,469 |
| olsen-crossdraft-36 | 1 | 1.10 | 30.6 × 30.6 × 32.6 | 2.5 | 66–287 | 12–130 | 78–417 |
| olsen-kit-100 | 1 | 4.37 | 55.7 × 55.7 × 55.7 | 2.5 | 262–1,135 | 39–860 | 301–1,995 |
| olsen-kit-16 | 1 | 0.93 | 25.9 × 25.9 × 41.2 | 2.5 | 56–242 | 8–139 | 64–382 |
| olsen-kit-24 | 1 | 1.27 | 34.6 × 34.6 × 34.6 | 2.5 | 76–330 | 15–207 | 91–538 |
| olsen-kit-50 | 1 | 2.37 | 44.2 × 44.2 × 44.2 | 2.5 | 142–617 | 25–406 | 167–1,023 |
| olsen-oil-drip | 1 | 1.62 | 36.0 × 36.0 × 42.5 | 2.5 | 97–421 | 16–269 | 113–690 |
| olsen-three-chamber | 3 | 12.76 | 50.2 × 50.2 × 52.3 each | 2.5 | 766–3,319 | 95–1,834 | 861–5,152 |
| olsen-two-chamber | 2 | 7.13 | 46.0 × 69.6 × 26.9 each | 2.5 | 428–1,853 | 81–666 | 508–2,518 |
| phoenix-nh | 1 | 1.13 | 32.6 × 32.6 × 29.4 | 2.5 | 68–294 | 13–147 | 81–442 |
| phoenix-wright | 1 | 0.25 | 16.3 × 16.3 × 15.2 | 2.5 | 15–66 | 3–18 | 19–85 |
| singh-coal | 1 | 6.66 | 42.0 × 42.0 × 51.1 | 2.5 | 399–1,731 | 22–428 | 422–2,159 |
| singh-lowfire | 1 | 2.78 | 35.7 × 35.7 × 53.0 | 2.5 | 167–723 | 16–309 | 183–1,032 |
| suzuki-kyoto | 7 | 78.88 | 160.3 × 41.5 × 55.3 each | 2.5 | 4,733–20,509 | 587–12,909 | 5,320–33,419 |
| tamba | 7 | 63.45 | 48.3 × 196.7 × 23.1 each | 2.5 | 3,807–16,497 | none | 3,807–16,497 |
| tobe | 7 | 443.95 | 291.0 × 94.3 × 83.5 each | 2.5 | 26,637–115,427 | 2,422–79,912 | 29,059–195,338 |
| updraft-test-1 | 1 | 1.53 | 24.0 × 36.0 × 57.5 | 2.5 | 92–397 | 11–239 | 103–637 |
| updraft-test-2 | 1 | 1.24 | 24.0 × 36.0 × 45.5 | 2.5 | 74–321 | 11–180 | 85–501 |
| updraft-test-3 | 1 | 2.12 | 36.0 × 36.0 × 57.5 | 2.5 | 127–550 | 16–359 | 143–910 |
| updraft-test-4 | 1 | 3.45 | 48.0 × 48.0 × 57.5 | 2.5 | 207–897 | 29–639 | 236–1,536 |

Checks (Derived): the kits' envelopes are `kit-stacking-space.md` §2's stackings (16: 25.9 × 25.9 ×
41.2 in; 24: a 34.6 in cube; 50: 44.2; 100: 55.7), as their design files were built round them;
the updraft tests' are their printed stackings (2 × 3 × 5 ft less the 2½ in under the shelf, p.74);
Kähler's its printed 24 × 24 in to the arch line. The 36 ft³ cross-draft's survey load, 150 kg
(`heat_cases.CROSSDRAFT_LOAD`), lies inside its band, 78–417 kg.

## 6. The setting's emissivity (Read: `radiation-exchange.md` §5.1)

Fired clay (63 % Al₂O₃) measured 0.54 at 1073 K and 0.52 at 1273 K (Jackson, Romero and Norris
1994, via Jones et al. [R6]); fireclay brick 0.75 at 980 °C (Sparrow and Cess, via Lienhard Table
10.1); fire brick, low alumina, 0.77 at 1273 K (Osborn 1985). No glazed ware or kiln shelf has a
measured hot emissivity in the sources read (`radiation-exchange.md` §4). The band: **0.52–0.77**,
the nominal **0.75** (fireclay brick). The survey's test input, 0.8, is above it; the fast-fire's
and the cross-draft's tests keep their inputs.

## 7. What stays open

- **No weighed studio setting** in an open source: the ware's band is industrial (whiteware and
  technical ceramics), the shelves' count a maker's kit. **A question for the owner**: should the
  band's heavy end take your own kiln's 2,600 lb of ware and shelves in 45 ft³ (926 kg/m³, about
  twice this band's top for that chamber)?
- **The setting as one box.** A round chamber's stacking is a cylinder (its inscribed square taken);
  a setting stepped up a climbing chamber's floor (Fujiwara's three levels, pp.102–103) or set in
  the flues between chambers (Hollyweird, p.116) is one box per chamber zone.
- **Posts** are left out (no source sizes them).
- **Pots by count** (Tamba's 500, Niñodaguia's 1000–3000) can't be weighed: no source gives those
  pots' masses.

## Sources

- European Commission, JRC, *Reference Document on Best Available Techniques in the Ceramic
  Manufacturing Industry*, August 2007: Tables 2.2, 2.7, 2.12, 2.17, 2.18, 2.22, 2.23, §2.3.8 and
  the glossary. Read from https://mepr.gov.ua/wp-content/uploads/2023/05/cer_bref_eng.pdf.
- J. S. Hohenshelt (Paragon Industries), "Kiln Firing Costs", 2009.
  https://www.artclayworld.com/v/vspfiles/assets/Tips&Techniques/KilnFiringCosts.pdf
- Skutt Kilns, FAQ (firing cost example) https://skutt.com/skutt-resources/resources-just-for-you/studio/faqs/ ;
  KM-1027 page https://skutt.com/?p=4184 ; "Furniture Kits" https://skutt.com/?p=13412.
- Skutt KM-1027 furniture kit contents: School Specialty (items 423191, 460262), Dick Blick
  ("Skutt Model 1027 3" Kiln Furniture Kit"), Chesapeake Ceramics ("1027 furniture kit"), listings
  read through a search engine's summaries, 2026-11-10 (the pages themselves refused the fetch tool).
- Advancer and silicon carbide shelf weights: Sheffield Pottery (ssfadv, ssfrc4128122434), Marjon
  Ceramics (ADV1224), Sounding Stone; CoreLite: The Ceramic Shop, Sheffield Pottery.
- Olsen, *The Kiln Book*, 4th ed., pp.33–35, p.74, p.76, pp.85–86, pp.102–103, p.116, p.131,
  p.135, p.136, p.139, p.142, p.148, p.153, p.160, pp.170–172, p.205.
