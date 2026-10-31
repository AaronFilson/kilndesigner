# Olsen, *The Kiln Book*, 4th edition: the kilns it describes

Frederick L. Olsen, *The Kiln Book: Materials, Specifications & Construction*, 4th edition. Read
from the user's scan, 2026-10-25 to 10-29 (see `kiln-reference.md` for scan coverage: pp.1–14,
190–193, 195 and 263–294 are not in the scan). This file lists every kiln the book describes, with
every number the book gives for it, so each kiln can become a design file. Pages are the book's
printed pages. Facts are paraphrased; quotes are kept very short.

How to read this file:

- Values are **as printed**, with their units. Nothing is rounded.
- **(drawing)**: read off a figure, not the text.
- **(?)**: uncertain reading of the scan.
- **derived**: arithmetic on printed numbers; the book doesn't print it.
- **Flagged**: the printed value looks wrong.
- **Not given:** what the book doesn't state that a design file would need. Never fill these from
  another kiln without a source.

Data classes in the index:

- **full**: enough to draw the kiln: chamber size, walls or roof, how it's fired, flues or chimney.
- **partial**: the chamber's size (dimensions or a printed volume) and some parts are known; others
  are not.
- **none**: the chamber's size can't be fixed from the book. Most of these are named or
  photographed only. A few have some part sizes (a firebox, a chimney section); those numbers are
  still listed, but the kiln can't be modelled without inventing its chamber.

---

## 1. Index

| id | Name | Pages | Fuel | Draft | Chamber shape | Size as printed | Data |
|---|---|---|---|---|---|---|---|
| **Gas box kilns and updrafts** | | | | | | | |
| `olsen-kit-16` | Olsen 16 kit (Bob and Sandy Kinzie) | 170, 173 | gas | updraft | box, sprung arch | "16 cu ft" (exit-flue rule); height 25 % over width | partial |
| `olsen-kit-24` | Olsen 24 kit | 139, 174, 221–222, 243 | gas (natural or propane) | updraft | box, sprung arch | 24 cu ft | partial |
| `olsen-kit-36` | Olsen 36 kilns (Scapin car kiln; Skælskør 1998) | 170–171, 182 | gas | updraft | box (car kiln) | model name only | none |
| `olsen-kit-50` | Olsen 50 car kiln | 170–171, 174 | gas | updraft | box (car kiln) | 50 ft³ (exit-flue rule) | partial |
| `olsen-kit-100` | Olsen 100 cu ft kit | 174 | gas | updraft | box | 100 cu ft | partial |
| `kaneko-car` | Jun Kaneko's car kiln | 170–172 | gas | updraft | cube (car kiln) | 500 cu ft; 8 × 9 × 8 ft | partial |
| `updraft-test-1` | Updraft test kiln, 2 × 3 × 5 ft-plus | 74 | gas (floor burners) | updraft | box | 2 × 3 ft base, 5 ft-plus stacking | partial |
| `updraft-test-2` | Updraft test kiln, 2 × 3 × 4 ft | 74 | gas (floor burners) | updraft | box | 2 × 3 × 4 ft stacking | partial |
| `updraft-test-3` | Updraft test kiln, 3 × 3 × 5 ft | 74 | gas (floor burners) | updraft | box | 3 × 3 × 5 ft stacking | partial |
| `updraft-test-4` | Updraft test kiln, 4 × 4 × 5 ft | 74 | gas (floor burners) | updraft | box | 4 × 4 × 5 ft stacking | partial |
| `olsen-crossdraft-36` | Olsen's 36 ft³ dense-brick cross-draft | 226 | gas | cross-draft | box | 36 ft³ | partial |
| `olsen-fiber-p62` | Olsen's cone-10 fibre kiln with cone anchors | 62 | not given | not given | not given | not given | none |
| **Downdrafts** | | | | | | | |
| `kahler-salt` | Nils and Herman Kähler's salt kiln, Næstved | 136–137 | gas (forced air) | downdraft, side-fired | box, sprung arch | 16 cu ft stacking | full |
| `blakebrough-tasmania` | Les Blakebrough's fibre envelope kiln, Tasmanian School of Art, Hobart | 69 (?), 148–150 | gas | downdraft | box on a track, flat fibre roof | 40 cu ft stacking; 42 × 54 × about 52 in | full |
| `bailey` | Bailey downdraft gas kiln | 150–151 | gas | downdraft | box | not given | none |
| `job-forni-gas` | Job Forni flat-roof fibre kiln, Cartigliano | 71, 150, 225 | gas | "downward draft" | box, flat roof | not given | none |
| **Fast-fire and other wood box kilns** | | | | | | | |
| `fast-fire` | Olsen fast-fire wood kiln | 139–143, 151, 199, 204–205, 213, 309 | wood | downdraft | box, sprung arch, fireboxes under the floor | 12 to 16 cu ft | full |
| `fast-fire-anderson` | Fast-fire at the Anderson Ranch, Aspen, 1977 | 141–142 | wood | downdraft | box, sprung arch | 18 cu ft | partial |
| `fast-fire-kecskemet` | Fast-fire kilns at the International Ceramic Studio, Kecskemét | 35, 141 | wood | downdraft | box | not given | none |
| `fast-fire-cappadocia` | Fast-fire salt kiln, Avanos, Turkey, 2008 | 143–145 | wood | downdraft | box, sprung arch | not given | none |
| `hacettepe-2004` | Two kilns at Hacettepe University, Ankara, 2004 | 143 | not given | not given | not given | not given | none |
| `finch-fast-fire` | Joe Finch's fast-fire variation | 146 | wood (gas, oil) | downdraft | box, sprung arch | not given | none |
| `phoenix-wright` | George Wright's Phoenix-style kiln, Portland | 147 | wood | firebox under floor, cross-draft chamber | box | 8 to 10 cubic foot (the user's reading) | partial |
| `phoenix-nh` | Phoenix workshop kiln, New Hampshire, 1978 | 147 | wood | downward draft | box | 40 cubic foot | partial |
| `salzer-phoenix` | Michael Salzer's portable Phoenix-style kiln | 147 | wood | downward draft | box, flat rowlock roof | not given | none |
| `bowen-mountain` | Olsen's Bowen Mountain salt kiln, Col Levy's studio | 127–128 | gas, oil drip or wood | cross-draft | box, sprung arch | 5 × 3 ft, 36 in to crown | full |
| `olsen-first-kiln` | Olsen's first kiln (Chappell's salt kiln design), Col Levy's, 1963 | 126–127 | crankcase oil and wood | cross-draft | not given | not given | none |
| **Chamber and climbing kilns** | | | | | | | |
| `hotchkiss-raw-clay` | Six-chamber raw-clay kiln (Richard Hotchkiss and a workshop group), 1971 | 33, 54–57 | not named (wood (?)) | climbing | chambers in series, arched | average chamber 5 × 5 × 6 ft | partial |
| `kyoto-climbing` | Kyoto-style climbing chamber kilns (type) | 89–94, 205 | wood | climbing (cross-draft chambers) | chambers in series, pointed arch | 6–7 ft tall, 4.5–6 ft wide | partial |
| `kyomizu` | Kyomizu climbing kiln, Kyoto | 89–91 | wood | climbing | chambers in series (10) | not given | none |
| `tobe` | Tobe Village kiln, Shikoku | 90, 92 | wood | climbing | seven chambers in series | 15,000 ft³; largest chamber 25 × 10 × 10 ft | partial |
| `onda-koishibara` | Onda and Koishibara kilns, Kyushu | 92 | wood | climbing | chambers in series | not given | none |
| `suzuki-kyoto` | Suzuki cooperative kiln, Kyoto | 93 | wood | climbing | seven chambers in series | chamber "(4.3 x 2 x 1.4m)" | partial |
| `bidai` | Kyoto Bidai climbing kiln, 1962 | 94–97, 200–201 | wood | climbing | firebox and three chambers in series | 19' 5" long; chambers 73" wide | full |
| `kawaii` | Takichi Kawaii's kiln, outside Kyoto, 1984 | 96–97, 200 | wood | climbing | four chambers in series | chamber 7 ft × 4 ft × 5 ft 8 in | partial |
| `fujiwara-bizen` | Kei Fujiwara's Bizen kiln, Imbe | 98–105 | wood | climbing (cross-draft) | fire mouth, himitsu, two chambers in series | dogi 8' × 10'; chimney 25 ft | full |
| `kanayama-bizen` | Commercial Bizen chamber kilns; Kanayama Pottery | 99, 105–106 | wood and charcoal | climbing | chambers in series | not given | none |
| `chappell-domura` | John Chappell's Domura tandem kiln (two-chamber kiln and salt kiln) | 33, 126, 243 | wood | cross-draft | two chambers in series, plus one salt chamber | 2 × 40 cu ft and 50 cu ft | full |
| `olsen-chamber-p23` | Olsen's chamber kiln (ring arch) | 23, 47 | not given | chamber | not given | not given | none |
| `olsen-two-chamber` | Olsen's two-chamber wood kiln, side-stoked | 202–203, 206 | wood | not stated | two chambers in series | first chamber 55" × 48" × 8' | partial |
| `olsen-three-chamber` | Olsen's three-chamber climbing kiln | 224 | gas (LP (?)) | climbing | three chambers in series | 3 × 120 cu ft | partial |
| `kitade-tojilo` | Kitade Tojilo chamber kiln, Kutani | 202–203 | wood | chamber (climbing) | chambers in series, arched | chamber 4' × 5' × 8' | partial |
| `blakebrough-sturt` | Les Blakebrough's kiln, Sturt Pottery, Mittagong | 205, 208 | wood and oil drip | chamber | chambers in series, arched | first chamber 6' × 45" × 6' | partial |
| **Tube, groundhog and tunnel kilns** | | | | | | | |
| `anagama-hole` | Anagama dug into a clay hill (type, Fig 4-5) | 83–84 | wood | cross-draft tube | tube on a slope | width 5¼', length 9–12' | partial |
| `tamba` | Tamba tube kilns, Tachikui | 85–88, 210 | wood (oil burners today) | climbing tube | tube on a slope | 120–150 ft long | partial |
| `bae-gilgama` | Mr Bae's Korean gilgama (Silla type), NCECA | 107–108 | wood | cross-draft, climbing | teardrop tube on a slope | 16' long | partial |
| `la-borne` | La Borne tunnel kilns, France | 109–111 | wood | tunnel (cross-draft) | tunnel on a slope | 1766 to 2825 cu ft | partial |
| `groundhog-basic` | Groundhog kiln (type, "basic dimensions") | 111–112 | wood | cross-draft | half-cylinder | 29–48 in high, 7–10 ft wide, 12–24 ft long | partial |
| `meaders-cheever` | Cheever Meaders's groundhog, Mossy Creek, Georgia | 112–113 | wood | cross-draft | half-cylinder | 48" to crown, 12' long | partial |
| `hart-square` | Hart Square groundhog (Kim Ellington, 1987), Vale, NC | 112–113 | wood | cross-draft | half-cylinder | not given | none |
| `ellington-new-hog` | Kim Ellington's "new hog" | 114–115 | wood (salt) | cross-draft | half-cylinder, tapering to the chimney | 24' overall, 10' wide | partial |
| `meaders-david` | David Meaders's groundhog | 115 | wood | cross-draft | half-cylinder | 5' × 6', 30" to crown | full |
| `hollyweird` | Olsen's Hollyweird Tube, 1985 | 116–117, 124, 194 | wood | cross-draft | two chambers in a tube | about 249 in to the chimney (derived) | partial |
| `gulgong-racer` | Olsen's Gulgong racer, Australia | 76, 118–121 | wood | cross-draft (groundhog) | cast dome | 106 cu ft; stacking 5 × 5 × 3½ ft | partial |
| `hohr-2003` | Anagama-style and fast-fire kilns, Höhr-Grenzhausen, 2003 | 122–123 | wood | cross-draft and downdraft | cast dome | not given | none |
| `conrad-teardrop` | Conrad Calimpong's teardrop kiln | 116, 124–125 | wood | cross-draft | teardrop plan, cast dome | inside length 9'9" | full |
| `kannofen` | Kannofen, Höhr-Grenzhausen | 161–164 | wood (salt) | updraught tunnel | tunnel, four arch sections | 4.5 m long; 1.04–1.07 m wide | partial |
| `olsen-anagama-p26` | Olsen's anagama-style kiln (K-26 hot face) | 26 | wood | cross-draft | not given | not given | none |
| `bayer-tube-form` | Svend Bayer's tube kiln over a slatted form | 50 | not given | tube | tube | not given | none |
| **Round, bottle and folk kilns** | | | | | | | |
| `pit-kiln-improved` | Improved pit kiln (type) | 152 | sticks, grass, dung | updraft | round, clay dome | wall 3'4", base "4'12"" | partial |
| `baobab` | Baobab-type kiln, Niger (type) | 153 | not given | updraft | round, shard dome | not given | none |
| `moveros-umbrella` | Umbrella kiln, Moveros, Spain | 153–154 | heather, brushwood | updraft | round | about 5 ft diameter, 4' tall | partial |
| `greek-updraft` | Early Greek updraft (type) | 154 | not given | updraft | round, dome | not given | none |
| `singh-lowfire` | Mansimran Singh's low-fire glaze kiln (early Muslim design), New Delhi | 155–156 | wood | updraft | round | 5' inside diameter, setting 5' | partial |
| `ninodaguia` | Niñodaguia kiln, northwest Spain | 156–157 | wood (pine) | updraft | round | 7' diameter, 3½' tall | partial |
| `miravet` | Miravet medieval kiln (old and new), Catalonia | 157–160 | wood | updraft | cube with dome over a sub-chamber cube | 8' × 8' I.D., 9' to crown | full |
| `falcone-pompeii` | Falcone Pompeii updraft, Montecorvino Rovella | 160–161 | wood | updraft | box, barrel vault, firebox below | 848 cu ft (3 × 4 × 2 m) | partial |
| `kenzan-muffle` | Kenzan enamel kiln (kin-gama), muffle | 165 | wood | updraft through a muffle | round muffle in a round kiln | muffle 2½' tall, 16–18" diameter | full |
| `bottger` | Böttger circular updraft, about 1700 | 166 | coal, coke | updraft | round, dome, cone chimney | not given | none |
| `breda-bottle` | Breda bottle kiln, Segra Pottery, 1979 | 166–168 | wood | updraft | round, dome, bottle chimney | chamber 15' diameter × 7' high | full |
| `bottle-two-storey` | Two-storey bottle kiln, mid-1800s (type) | 168–169 | coal, coke | updraft | round, two storeys | not given | none |
| `sevres` | Sèvres two-storey bottle kilns | 168–169 | not given | updraft | round, two storeys | not given | none |
| `milton` | Milton's two-chamber kiln, England, 1873 | 169 | not given | updraft and downdraft | two chambers | not given | none |
| **Multi-directional** | | | | | | | |
| `fireworks-edmonton` | Fireworks kiln, Edmonton, 1998 | 178–181, 183 | wood | multi-directional | cast dome over two crossing axes | fire zone about 9 ft | partial |
| `church-skaelskor` | Church kiln, Skælskør (Guldagergaard), 1998 | 180, 182–183 | wood | multi-directional | two crossing axes | fire zone 7 ft | partial |
| `kecskemet-multi` | Kecskemét kiln, International Ceramic Studio | 182–183 | wood | multi-directional | two crossing axes | "larger" than 9 ft | none |
| `kanayama-multi` | Kanayama multi-directional kiln | 183–189 | wood | multi-directional | cast dome over two crossing axes | 16 shelves in the fire zone | none |
| **Electric** | | | | | | | |
| `electric-car-45` | Widest electric car kiln Olsen knows | 244–245 | electric | — | box (car kiln) | 45 × 106 × 49 in inside | partial |
| `jiesia` | Jiesia bone-china car kilns, Kaunas | 245 | electric | — | box (car kiln) | not given | none |
| `job-forni-hobbyker` | Job Forni "Hobbyker" front-loaders | 248 | electric | — | box | not given | none |
| `electric-reduction-smoke` | Electric kiln with a wood smoke firebox | 250 | electric, wood smoke | updraft (smoke) | box | not given | none |
| **Oil and coal** | | | | | | | |
| `kato-coal` | Mr Kato's coal downdraft, Tajimi | 131–132, 207 | coal (later oil) | downdraft | box with bowed walls, arched | about 250 cu ft; 6'6" × 7' (?) × 6'6" | full |
| `singh-coal` | Mansimran Singh's round downdraft, Delhi Blue Pottery | 133–135, 207 | coal | downdraft | round, dome | 11 m³; 7' diameter | full |
| `kanayama-oil` | Kanayama oil downdraft (Olsen, 2005) | 137–138 | oil | downdraft | box, sprung arch | not given | none |
| `olsen-oil-drip` | Olsen's gravity-drip oil kiln | 207–209 | #2 diesel | not given | not given | 45–60 cu ft | partial |
| `leach-chamber` | Bernard Leach's chamber kiln | 210, 213 | oil | chamber | chambers in series | not given | none |
| `park-tuscarora` | Denis Park's Tuscarora drain-oil kiln | 209–210, 224 | crankcase oil | not given | not given | not given | none |
| `soldner-raku` | Paul Soldner's raku kiln | 210 | kerosene | not given | not given | not given | none |

Named only, not counted as kilns above (no description beyond a name): Soldner's catenary design,
Nils Lou's Minnesota Flat Top, Geil Kilns, Rohde, Nabertherm (p.150; the Minnesota Flat Top also
p.76); "some professionally made gas pseudo-downdraft kilns" (p.76); small corbel-arched kilns of
10 to 16 ft³ Olsen has seen (p.49); Chien Yao and Seto kilns (p.90, saggar history); La Borne,
Cassel and Newcastle kilns as the groundhog's roots (pp.111–112); Burlon Craig's kiln, early 1930s,
whose arch boards Ellington reused (p.113).

Count: 88 kilns: 14 full, 41 partial, 33 none (`phoenix-wright` moved to partial when the user
read its volume, 2026-10-29).

---

## 2. Gas box kilns and updrafts

### Olsen Kiln Kits: what all the kits share

Not a kiln: the facts the book gives for the kit family, which apply to `olsen-kit-*` below.

- Olsen Kiln Kits, started 1973 (pp.169–170): patented designs of 12 to 120 cu ft (0.34 to 3.4 m³)
  of stacking space; IFB; natural gas or propane; sold with a pre-welded frame, bricks, burners,
  burner manifolds and parts. Any size can be had as a car kiln.
- Draft: updraft, "forced draft" by gas pressure (p.170).
- IFB 2500/2600 laid in Harbison-Walker Sairset air-set mortar (p.32).
- Burners: Gas Appliance MR-750 and MR-100, 75,000 and 100,000 BTU/hr at 8 in. WC (p.222).
- No fibre in the kits (p.175, Fig 6-72).
- Manifolds for updrafts up to 72 ft³: 1¼ × 1¼ in or 1¼ × 2 in channel tubing bent round the
  corners; up to 20 burners on one manifold, sized for all burners plus 20 % (p.235, Fig 8-57).
- Design rules stated for these updrafts: cube chamber, height up to 25 % more than the width
  (p.170); exit flue equal to the inlet area is "more than adequate" up to 40 cu ft (p.173; p.174
  says 36 ft³, see `kiln-reference.md` §5); above 5000 ft, equal inlet and exit up to 40 cu ft and
  a 20 % larger exit above that (p.174).

### `olsen-kit-16`: Olsen 16 kit, Bob and Sandy Kinzie

- Pages: p.170 (text, Fig 6-59 photo); p.173 (text).
- Fuel: gas (kit). Draft: updraft. Cone and firing time: not given.
- Chamber: height 25 % greater than width; "fires quite evenly" (p.170). Volume 16 ft³ by its name;
  p.173 gives the starting exit flue "for a 16 cu ft (0.45 m³) kiln".
- Exit flue: 40½ sq in (261 cm²) to start (p.173).
- **Not given:** width, depth, height; inlet area; burner count and rating; walls; roof; frame; door;
  damper.

### `olsen-kit-24`: Olsen 24 kit

- Pages: p.139 (text); p.174 (text); pp.221–222 (text, Fig 8-43); p.243 (text).
- Fuel: gas; natural gas or propane. Draft: updraft.
- Size: 24 cu ft (0.68 m³) (p.174).
- Burners: eight perimeter burners and two bottom burners (p.174). The kits use MR-750 and MR-100
  burners (p.222); which one the 24 uses isn't said.
- Inlet: 50 sq in (323 cm²) in all (p.174). Ten round ports of 2½ in give 49.1 in² (derived; the
  port size isn't printed for this kiln, but Fig 3-12's example uses 10 ports of 2½ in, p.78).
- Exit flue: 45 sq in (290 cm²) (p.173, p.174). A 50 sq in exit "can be used", with the damper
  blocking the extra area (p.174).
- Firing: Olsen's own "Olsen 24 updraft gas kiln" fires in eight hours, some glazes in four (p.139).
- On propane (p.221): he kept the natural-gas orifice, **#32**, cut the tank pressure to under 1 lb
  (1 psi) and ran at most **4 in. WC** at the kiln: a longer flame and better distribution. He
  doesn't recommend it (raw gas can be forced through without a tank regulator below 1 psi; firing
  costs more).
- Installation (p.243): a kit in a friend's studio, under a 7 ft (213 cm) ceiling against Olsen's
  advice; the roof caught fire in the second firing.
- **Not given:** width, depth, height; port size; burner model; walls; roof; frame; door; damper;
  cone.

### `olsen-kit-36`: Olsen 36 kilns

- Pages: p.170 (caption 6-62), p.171 (photo); p.182 (text).
- Giancarlo Scapin's Olsen 36 car kiln, Schio, Italy (caption 6-62). One Olsen 36 gas kiln was built
  at the 1998 Skælskør workshop (p.182).
- Fuel: gas. Draft: updraft.
- **Not given:** everything else. The 36 ft³ IFB updraft "with a minimum of 10 such burners" on
  p.226 is a general statement, not said to be this kit (worked example W15).

### `olsen-kit-50`: Olsen 50 car kiln

- Pages: p.170 (caption 6-61), p.171 (photo); p.174 (text).
- Fuel: gas. Draft: updraft car kiln.
- Exit flue: 90 sq in to start for 50 ft³ (p.174). Kilns over 50 cu ft (1.42 m³) "require larger
  exit flues in order to fire evenly" (p.174).
- **Not given:** dimensions, inlet area, burners, walls, roof, car, door, frame.

### `olsen-kit-100`: Olsen 100 cu ft kit

- Page: p.174 (text).
- Size: 100 cu ft (2.83 m³). Fuel: gas. Draft: updraft.
- Inlet flues: 100 sq in (645 cm²). Exit flue: a minimum of 120 sq in (774 cm²), up to 140 sq in
  (903 cm²).
- **Not given:** dimensions, burners, walls, roof, frame, door.

### `kaneko-car`: Jun Kaneko's car kiln

- Pages: p.170 (text, Fig 6-60 photo); p.171 (text); p.172 (text, Fig 6-64).
- Fuel: gas, atmospheric burners. Draft: updraft. Cube shape.
- Size: **500 cu ft (14.16 m³)** (p.170). Chamber 8 ft (244 cm) tall, 9 ft (274 cm) deep, 8 ft
  (244 cm) wide; cart 7 ft (213 cm) wide (p.171). 8 × 9 × 8 ft = 576 ft³ (derived), so the 500 is
  probably stacking space.
- Burners: 32 atmospheric burners, ten on each side and six each at front and back. Combustion width
  9 in (23 cm), standard burner-port spacing (p.172).
- Door: hung from an overhead I-beam on two Yale half-ton trolleys, with U-bolts and eye-bolts;
  spring-tension latches pull it into the jambs (Fig 6-64).
- Firing: extremely slow, a long soaking rise over several days.
- **Not given:** burner rating and gas; walls; roof (arch or flat); exit flues; damper; frame;
  car construction; cone.

### `updraft-test-1` to `updraft-test-4`: the updraft test kilns behind Design Principle 1

- Page: p.74 (text, second scan). Fuel: "burners in the floor" (gas implied). Draft: updraft.
  Sizes are stacking space.
- `updraft-test-1`: base 2 × 3 ft (61 × 91 cm), "5ft (152cm)-plus-high" stacking: ½ to 1 cone
  difference top to bottom, whatever the schedule. At least 30 ft³ (derived).
- `updraft-test-2`: the same kiln 1 ft shorter, 2 × 3 × 4 ft (61 × 91 × 122 cm): "perfectly even".
  24 ft³ (derived).
- `updraft-test-3`: "a similar kiln", 3 × 3 × 5 ft (91 × 91 × 152 cm): "a constant ½ to 1 cone
  difference". 45 ft³ (derived).
- `updraft-test-4`: test 3 with width and length raised to 4 ft (4 × 4 × 5 ft): evened out
  perfectly. 80 ft³ (derived).
- Olsen's conclusion: with floor burners, equal height and width matter most (p.74).
- **Not given:** walls, roof, burner count and rating, flues, cone, firing time, who built them.

### `olsen-crossdraft-36`: Olsen's 36 ft³ dense-brick cross-draft

- Page: p.226 (text; also in `kiln-reference.md` §4).
- Size: 36 ft³. Dense brick. Fuel: gas (type not given). Draft: cross-draft.
- Burners: six small venturi air-mixer burners at 36,000 BTU/hr each; fired in about 12–15 h.
  6,000 BTU/ft³/hr (derived), well under his own 16,000 minimum for dense brick.
- **Not given:** dimensions, wall thickness, roof, ports, flues, chimney, cone.

### `olsen-fiber-p62`: Olsen's cone-10 fibre kiln with ceramic cone anchors

- Page: p.62 (text).
- Fired twice daily to cone 10, seven days a week. Kao-Lok ceramic cone anchors on Inconel studs:
  where the fibre packing in the cone leaked, the stud oxidized and was destroyed. Screw-in plugs
  dipped in mortar or Kaowool cement slowed this but "didn't last long".
- **Not given:** fuel, draft, size, lining layers.

---

## 3. Downdrafts

### `kahler-salt`: Nils and Herman Kähler's downdraft salt kiln, Næstved, Denmark

- Pages: p.136 (text, Figs 5-17 to 5-21); p.137 (text).
- Fuel: gas, "Forced gas burners" (drawing), "a forced air/gas type mounted into super-duty port
  blocks" (p.137). Salt glaze. Draft: downdraft, side-fired.
- Size: "16cu. ft (0.45cu. m) stacking space" (p.136).
- Chamber, front section Fig 5-17 (drawing): inside width 30" wall to wall; 24" between the
  dashed stacking lines; outside width 45"; 39" from the floor to the upper front burner.
- Chamber, side section Fig 5-18 (drawing): inside height 48" (floor to arch line); depth 36" wall to
  wall and 24" stacking; a "40½"" from the left outer line to a point short of the right outer face,
  which is less than 36" + 2 × 7½" = 51" (derived), so it measures something else (what, the
  drawing doesn't show). The 24", 36" and 40½" figures and the channel label below Checked on the
  page image, 2026-10-31.
- Walls: "All walls 7½" thick" (drawing); high-alumina insulating refractories against salt slag
  (p.136). Drawing note: "All light-weight insulation High Al₂O₃ bricks or dense Al₂O₃ bricks with 8"
  walls".
- Roof: sprung arch (drawing). Span, rise and thickness not given.
- Floor: the floor slab stands 4½" clear of the walls, so gas passes round its edge into the
  channels below (Fig 5-18).
- Burners: four by the drawings, two per side wall, staggered: front (left) at 18" and 39" above the
  floor; back (right) at 9" and 28" (Figs 5-17, 5-19). Port blocks "K28 dense high Al₂O₃ block".
  The front burners sit high above the exit flue, the back burners lower, midway between the
  opposing ports, for a clockwise rolling flame (p.137).
- Exit flues: "EXIT FLUES 4½" X 9"" in the floor (three drawn); "COLLECTION FLUE CHANNELS 4½" X 9"
  each" (Fig 5-18).
- Chimney: "CHIMNEY FLUE – 9" X 7" max" through the crown; "Chimney height 10–12'" (drawings).
- Salt ports: in the arch, top front and top back; the back port salts over the right middle top
  burner, the front port into the left front top burner's flame (p.137).
- Door: in the side, with three "SPY AND DRAW HOLES" (Fig 5-18).
- **Not given:** burner rating, gas, pressure, orifice; arch span, rise, thickness; channel layout
  under the floor; damper; steel frame; cone; firing time.

### `blakebrough-tasmania`: Les Blakebrough's fibre envelope kiln, Tasmanian School of Art, Hobart

- Pages: p.148 (text, Figs 5-70 to 5-73); p.149 (text, Figs 5-74 to 5-79); p.150 (named "the
  Tasmanian envelope kiln", the model true downdraft). p.69 describes a large folded-fibre kiln at
  the Tasmanian School of Art with Blakebrough; the book doesn't say it is this kiln (probably the
  same: both compress the fibre with a board).
- Fuel: gas (type not given). Draft: true downdraft, through the floor into a collection channel and
  up the chimney (p.150).
- Size: "A 40 cu. ft (1.13cu. m) stacking envelope-style downdraft fiber box kiln" (p.148). Started
  from a cube, adjusted for shelves and burner channels: interior hearth 42 in (107 cm) wide by 54 in
  (137 cm) long, about 52 in (132 cm) high, for two 24 × 24 in (61 × 61 cm) shelves (p.148). 42 × 54 ×
  52 in is about 68 ft³ gross (derived).
- How it moves: a fixed hearth joined to the back wall and chimney; the box chamber runs in on a
  track over the hearth and seals against the back wall (p.148).
- Walls and roof: fibre on expanded metal mesh inside the frame; a suspended flat fibre roof fitting
  down onto the three side walls, fixed to the corner legs (p.148, Fig 5-75). Hearth, flue channels,
  chimney base and the first 15 in (38 cm) of the chamber are 2600 IFB (p.148). The fibre is
  compressed by a board worked by an expansion jack (captions 5-76, 5-77). p.69 (same kiln (?)):
  folded blanket, each 12 in (30.5 cm) compressed to 8 in (20 cm) by a hydraulic ram on a full-wall
  board; stainless rods tacked to the frame at 12 in (30.5 cm) intervals up the wall.
- Hearth (Fig 5-72, drawing): inside 42" × 54"; outside 45" (Checked on the page image, 2026-10-31; the drawing puts the 42"
  along the top edge of the same face, so which is inside is the text's reading); hearth wall "15" OR 5 BRICKS";
  "9" WALLS"; on concrete block; track alongside.
- Burners: four "Venturi compound injector burners", each with its own safety and ignition system
  (p.149). Two burner ports, 4½ × 6 in (11.5 × 15 cm), in the back wall, with opposing ports firing
  down 9 in (23 cm) side-burner channels (p.149). Fig 5-72 draws two BURNER CHANNELs 4½" wide with a
  9" strip between them, burner ports in their floors (four per channel drawn), and a separate
  burner-port block at the back. The two notes read the text and the drawing differently; both are
  given here.
- Flues: eight floor exit flues formed by bricks laid over the flue channel (p.149). "Two 4½in.
  (11.5cm) flue channels, 9in. (23cm) apart and 6in. (15cm) deep, funnel into a chimney flue (9 x
  6in./23 x 15cm) leading to a 9 x 9in. (23 x 23cm)" chimney (p.148). Fig 5-72: "FLUE CHANNELS 4½"
  WIDE X 6" DEEP".
- Chimney: 9" × 9", with a damper slab on top (Fig 5-72).
- Setting: shelves raised off the floor, a 9 in burner channel along the side of the shelves
  (Fig 5-70).
- **Not given:** burner rating, gas, pressure; chimney height; fibre thicknesses and grades; frame
  sizes; cone; firing time.

### `bailey`: Bailey downdraft gas kiln

- Pages: p.150 (text, Fig 5-80 photo); p.151 (text).
- Bailey Gas Kilns, Kingston, New York (from 1983). A box kiln with its door open (photo). A
  ventilation collection hood and stack take over above the chimney (p.151).
- **Not given:** any dimension.

### `job-forni-gas`: Job Forni flat-roof fibre kiln, Cartigliano, Italy

- Pages: p.71 (text); p.150 (text); p.225 (Fig 8-49).
- An industrial flat-roof fibre kiln Olsen used there, with top and bottom side burner ports and
  tempered-air burners; "downward draft" in his terms (p.150). The maker builds with
  accordion-folded modular fibre (p.71; which kiln isn't said).
- Job Forni tempered-air burner (Fig 8-49, drawing): mixing cylinder 2¾" inside diameter (read by the user, 2026-10-31; the drawing sets no outside diameter for the cast-ceramic part) × 2" deep
  I.D.; cast-ceramic nozzle through the kiln wall, 6" long, 2" taper, 1½" tip, about 2¾" body;
  spark plug.
- **Not given:** size, burner count and rating, flues, chimney.

---

## 4. Fast-fire and other wood box kilns

### `fast-fire`: Olsen's fast-fire wood kiln

- Pages: pp.139–143 (text, Figs 5-35 to 5-47); p.151 (text); p.199 (text); pp.204–205 (text,
  Figs 8-13, 8-14); p.213 (text); p.309 (firing log). `kiln-reference.md` §2, §5, §6 cite its frame,
  chimney rule and firebox rules.
- Builder: Olsen. Built at many workshops (see the next four entries).
- Fuel: wood, "a quarter of a cord of wood of any kind" (p.139); "less than a quarter of a cord of
  wood for a 3½ to 4-hour firing" (p.143). The design can be built for gas or oil (p.142).
- Draft: downdraft. Two fireboxes under the floor in an "S" plan, inlet flues up into the chamber,
  exit flue at floor level in the back wall into the chimney.
- Cone and time: cone 10 in 3½ hours (p.139). Firing log (p.309): cone 10 in a "Total Time: 4 hours
  and 45 minutes", called slow (the log runs 4:55 to 9:45, 4 h 50 min, derived); the same design at
  Olsen's studio, 6000 ft, reached cone 10 flat in 1 h 55 min (fired with Les Blakebrough).
- Size: "a 12 to 16cu.ft kiln (0.34 to 0.45m³)" (p.140). Family: 12 to 45 cu ft (0.34 to 1.27 m³)
  (p.139); can be enlarged to 12–120 cu ft (0.34–3.4 m³) by enlarging the cube with the inlet flues,
  exit flue and chimney (p.142). An all-hard-brick 40 cu ft (1.13 m³) kiln averages 12 to 14 hours
  (p.143).
- Chamber (Fig 5-35, drawing): inside width 27"; height 36"–40" from floor to springline (by the
  arrow). Depth not printed. A 27 × 27 × 38 in box is about 16 ft³ (derived).
- Walls (p.140): one brick thick, 2300 °F (1260 °C) IFB 4½ in (11.5 cm), backed by flexboard or a
  similar rigid board, or sheet metal if no board. The back wall goes up past the arch; the door
  rowlocks go up past the arch.
- Roof: "4½" ARCH" of 2300° IFB (Fig 5-35); standard featheredge skewbacks; a bonded arch of No.1 arch
  bricks with straights, laid on a form; the arch butts the back wall (p.140). Span 27" (derived from
  the width). Rise not printed (a featheredge skewback gives 1½ in per ft, `kiln-reference.md` §1).
- Floor and bag wall: the setting on the floor "Acts as bagwall"; "First row is rowlock to make floor
  exit channel" (Fig 5-35). A rowlock row along each inlet-flue edge, back to front, carries the first
  shelf and is the bag wall; two rows high is enough; tight near the flue, more open away from it
  (pp.141–142; Fig 5-44 "ROWLOCK BRICK 4½" SOLID ACROSS FROM FRONT TO BACK").
- Shelves: "12" X 24" X 1 SHELVES" (Fig 5-35; Checked on the page image, 2026-10-31). Layout: 4½ in (11.5 cm) clear each side (over the
  inlet flues) and in front, 1 in (2.5 cm) between shelves and at the back (p.142, Fig 5-43; the
  front label reads "4½"–5"", read by the user, 2026-10-31; Fig 5-43 is on p.141). p.151 says the fast-fire kiln uses a 4 in (10 cm) front space: the
  two pages differ by ½ in.
- Fireboxes: two of equal size under the chamber, along the front and back walls, each 13½ × 40½ in
  (34 × 102 cm) "or whatever the width of the kiln is" (p.204); 12–15" high (Fig 8-13, drawing). Text
  p.140: "1½ bricks wide and 4½ deep and 6 bricks tall"; Fig 5-39 draws five courses, with a sixth
  added only "for high altitude" (**Flagged**: five or six courses; the user reads Fig 5-39 as five
  courses, a sixth at altitude, 2026-10-29). p.199: the shortest firebox,
  12½ in with the grate at 6–7 in, is for a 12–16 ft³ fast-fire kiln. More than half the firebox is
  below the grate (p.140).
  - Built of straight hard firebrick: "LOW DUTY FIREBRICK 90 required"; "Add 6th row for high altitude
    109 bricks required" (Fig 5-39).
  - Foundation 45" (5 bricks) × 40½" (4½ bricks); two firebox channels 13½" wide in an S, one open at
    each end, each with its chamber inlet flue at the closed end (Fig 5-37).
  - Spanned with kiln shelves, "18" X 18" MULLITE SHELVES" (Fig 5-39), or bricks or a castable
    (p.141); the gap round the inlet flue shimmed to shelf level (p.140).
  - Two fireboxes 13½ × 36 in give 972 in², 10 × the 81 in² chimney plus 20 % (derived; the p.140
    rule).
- Inlet flues: "CHAMBER INLET FLUES 4½" X 13½"" (Fig 5-39); "4½in./11.5cm x the width of the firebox",
  at the end of each firebox (p.141); a 4½" slot along the top (Fig 8-13).
- Grate: pull-out. "FIREBOX GRATE 24–27" LONG, 12–13" WIDE, 7–8" TALL" (Fig 5-39). Fig 8-13: welded
  ¾ in (2 cm) iron rod at 1½" on centre (¾" clear); grate 12" × 24"; legs 7–8" tall, 12" apart. It
  bisects the firebox and sits as far back as possible, partly under the inlet flue (p.204). Pull the
  grates after firing or they oxidize and warp (p.204). Permanent alternative: a ledge at half height
  carrying ceramic tubes or posts at 1 in (2.5 cm) spacing, two-thirds of the way in (p.205).
- Exit flue: 9" × 7½" (Fig 5-35); 13½" × 7½" at high altitude. The walls are tied to the chimney to
  form the exit flue "(1 brick square)" (p.140). Floor exit channel 4½" high (Fig 5-47). A "trick
  brick" opens an upper flue above the first shelf if needed (Fig 5-47, p.142; label "EXIT FLUE 13½" X
  7½"", faint, agreeing with Fig 5-35's high-altitude "13½" x 7½"": Checked on the page image,
  2026-10-31).
- Chimney: "CHIMNEY 9" X 9" X 14'" (Fig 5-36); "9" X 9" X 14' TALL, increase to 13½" X 13½" for high
  altitude (Made from chimney flues)"; "40 BRICKS FOR CHIMNEY FOUNDATION" (Fig 5-37). The platform is
  built up level with the firebox top (p.140). A passive damper air hole can go in the back of the
  chimney (p.141). Height rule: 3 × (chamber + firebox height) plus 1 ft per 3 ft of horizontal run
  (p.140; see `kiln-reference.md` §5 on the reading).
- Steel frame: angle iron 2 × 2 × 3/16 in, bolted; flexboard inside the frame (Fig 5-36).
- Door: "DOOR LAID IN ROWLOCK" (Fig 5-35); bricked up with stretchers (4½ in) or rowlocks (2½ in);
  pull-out cone-hole plugs; a hole about 2½ × 2½ in left open at the top centre (p.141).
- Gas version (p.142): gas ports 4½ × 4½ in (11.5 × 11.5 cm) at floor level in the side walls, in
  removable bricks (four per side drawn, Fig 5-46); block the inlet flues and mud-seal the firebox
  mouth; burners by Chapter 8. Oil: drip plates or forced-oil burners in the firebox (p.142); the
  firebox suits forced oil (p.213).
- Firing method (pp.139, 142–143): fire one firebox to a coal bed, start the other at about 1100 °F
  (590 °C), then alternate; never full-stoke both; after the first hour, 4–6 kindling-size pieces
  about every 3 minutes per side. Critical (choking) temperatures about 1100 °F (590 °C) and 1994 °F
  (1090 °C). Never let the coals under the grate touch it. Soak at the end; a half-hour soak for
  saggared or tight settings; cool slowly, especially from 1100 °F/590 °C to 200 °F/90 °C.
- Firing log, p.309 ("Table A-1", a misnumbered table), time, °C, note: 4:55 start, damper ¾ closed,
  one firebox on kindling; 5:00 190; 5:15 315; 5:30 455; 5:45 580, start the other firebox; 6:00 720;
  6:15 790, damper ½ open; 6:30 900; 6:45 955; 7:00 1016, "Cone 6 down" (**Flagged**: at 1016 °C it
  must be cone 06); 7:15 1050; 7:30 1095; 7:45 1105; 8:00 1180, cone 5 down; 8:15 1205, damper ¾
  open; 8:30 1235, cone 9 bending; 8:45 1260, cone 9 flat; 9:00 1285, cone 10 down, trick brick in;
  9:15 1285, damper fully open; 9:30 1285, stoking to hold; 9:45 1285, done, damper and fireboxes
  closed.
- **Not given:** chamber depth; arch rise; damper size; door frame.

### `fast-fire-anderson`: fast-fire kiln at the Anderson Ranch, Aspen, Colorado, 1977

- Pages: p.141 (Fig 5-41 photo); p.142 (text, Table 5-2).
- Workshop, summer 1977. "An 18 cu. ft (0.51cu. m) Olsen fast-fire wood downdraft", IFB, bricked-up
  door (Fig 5-41).
- First firing (Table 5-2): fire under the grate in the front firebox about 2.30 pm, on the grate an
  hour later; 4.00 pm 500 °F/260 °C; 5.00 pm about 1000 °F/538 °C; 6.00 pm 1250 °F/677 °C, damper ¼
  open; 7.15 pm 1400 °F/760 °C, damper ½ open; 7.30 pm back firebox started; 8.15 pm 1600 °F/871 °C;
  9.30 pm 1820 °F/993 °C, damper ¾ open; 10.00 pm cone 8 down at the bottom; 10.30 pm cone 10 soft,
  soaking; 12.30 am cone 10 down everywhere; 12.45 am shut down. About 10 h (derived).
- **Not given:** its own dimensions (presumably the design above, not stated); chimney; elevation
  (Aspen is 8600 ft, p.82, read by the user, 2026-10-29; digits cut in the scan).

### `fast-fire-kecskemet`: fast-fire kilns at the International Ceramic Studio, Kecskemét, Hungary

- Pages: p.35 (text); p.141 (text, Fig 5-42).
- Thin nitride-bonded SiC shelves from a porcelain factory cracked near the inlet flue and in the
  direct flame, from the fast rise and the burst of heat after each stoking (p.35). The two Olsen
  fast-fire kilns at ICS use a swing door (p.141).
- **Not given:** sizes. (Not the multi-directional `kecskemet-multi`.)

### `fast-fire-cappadocia`: fast-fire salt kiln, Avanos, Turkey, 2008

- Pages: p.143 (text, Figs 5-48, 5-49); p.144 (photos); p.145 (captions, left ends lost).
- 6th International Applied Ceramic Symposium (Emre Feyzoğlu and Kaan Canduran). Wood; salt.
  Downdraft (fast-fire design). Dimensions were "developed around the available kiln shelves".
- Built on a platform of building blocks, cores filled with sand, to put the fireboxes at sitting
  height (caption 5-49). 'S' firebox channels; firebrick floor on the blocks; rowlocks span the
  firebox width with a middle support, or circle bricks span it (captions 5-50 to 5-52). "9in.
  ([23c]m) walls are used" (caption 5-53). Four rowlock bricks for the door space; a damper slot
  spanned in the chimney; featheredges cut from soft bricks; a bonded arch of straight bricks in
  fireclay mortar, wedged at the crown with broken brick (captions 5-54 to 5-58). Angle-iron bracing;
  salt ports in the back wall, bottom and top (5-60). First firing: about half a cone between top and
  bottom (5-62).
- **Not given:** any chamber, firebox, flue or chimney size.

### `hacettepe-2004`: two kilns at Hacettepe University, Ankara, 2004

- Page: p.143 (text). A workshop led by Olsen (Emre Feyzoğlu): two kilns for the Ceramics Department,
  one a salt kiln.
- **Not given:** everything else.

### `finch-fast-fire`: Joe Finch's fast-fire variation

- Page: p.146 (text, Figs 5-63 to 5-66), from Finch's *Kiln Construction* (A&C Black).
- Wood; "can be adjusted for wood, gas or oil firing". True downdraft. Keeps the 'S' fireboxes but
  leaves the space between them open as the exit-flue channel; the chimney is in line with the
  fireboxes, offset from the firebox entrance; 3 in (7.5 cm) ceramic tubes as widely spaced grate
  bars in the middle of the firebox; kiln shelves as the floor; angle-iron frame (tie rods across the
  top in the photos); arch on a form; a built-up door. Passive-air damper pull-out bricks at the
  chimney base (Fig 5-64).
- **Not given:** any dimension.

### `phoenix-wright`: George Wright's Phoenix-style kiln, Portland, Oregon, 1970s

- Page: p.147 (text). "A small 8 to 10 cubic foot wood-fired kiln with a Roman arched firebox under
  the kiln [floor] with a cross-draft chamber above" (the "10", lost in the gutter in the scan, read
  by the user, 2026-10-29).
- **Not given:** the upper volume and every dimension.

### `phoenix-nh`: Phoenix workshop kiln, New Hampshire, 1978

- Page: p.147 (text, Fig 5-67). Documented by Gerry Williams, *Studio Potter*, Vol. 7, No. 2. Town
  printed "[…]barton" (first letters lost in the gutter).
- "A 40 cubic foot variation" of Wright's kiln; the name Phoenix comes from it. Wood.
- Layout (Fig 5-67, no dimensions): Roman-arch firebox under the chamber floor with grate bars; inlet
  flue rising at the front of the chamber; draft over and down to an exit flue at floor level at the
  back; the chimney shares the chamber's back wall.
- **Not given:** every dimension.

### `salzer-phoenix`: Michael Salzer's portable Phoenix-style kiln

- Page: p.147 (text, Figs 5-68, 5-69). Salzer Kilns, Kaub, Rhein, Germany; fired at the Brollin
  Woodfire Conference.
- Wood. A flat roof of rowlock bricks held in an iron frame; one firebox on the back side under the
  chimney and the kiln-shelf floor; one inlet flue at the front; exit at the back at floor level;
  chamber and chimney share a wall. Photos: IFB walls, tie rods, several dampers on the chimney top.
- **Not given:** any dimension, cone or firing time.

### `bowen-mountain`: Olsen's Bowen Mountain salt kiln, Col Levy's studio, Australia

- Pages: p.127 (Figs 4-152, 4-153); p.128 (text, Figs 4-154, 4-155). A revised Chappell design.
- Fuel: three firebox options drawn, 1 gas, 2 oil drip, 3 wood, "with fuel combinations possible"
  (p.127). Salt glaze. Draft: cross-draft: front firebox and bag wall, exit flues to a flue
  collection box, then the chimney.
- Cone: salting starts at cone 9–10 (p.128).
- Chamber (drawing): 5' long × 3' wide inside; 36" floor to crown; the arch comes down at the back to
  18" above the floor (Checked on the page image, 2026-10-31). "WIDTH CAN EXTEND TO 4 FEET WITH ADDED FLUES – AND ADJUSTMENT TO WOOD FIRE
  BOX – STOKE BOTH SIDES". "An overall chamber length of at least 48in. (122cm) would help to even up
  the firing" (p.128).
- Walls: "9" WALLS" (plan). Roof: arch with bracing on its front (drawing); span 3' (derived), rise
  and thickness not given.
- Firebox: across the front, 12" below the chamber floor (Checked on the page image, 2026-10-31);
  "BURNER OR STOKE HOLE"; bag wall in front of it.
- Inlet flues: gas 9" × 4½"; oil drip or wood 13½" × 4½"; four openings drawn in the plan's front
  wall (Checked on the page image, 2026-10-31; first read as three). `bowen-mountain.yaml` now has
  eight burners, two per flue.
- Detail 1, gas: "2 GAS BURNERS PER FLUE", "MR 750 BURNERS", "4½" X 7" FLUES": 4½ × 9 in as
  drawn, the printed 7 a misprint (read by the user, 2026-10-31);
  an IFB block 9" × 4½" with two "2½" HOLES" for the burners.
- Detail 2, oil: "DRIP PLATES", "13½" X 4½" FLUES".
- Detail 3, wood: stoke hole 13½" wide and 13½" high; "4½" X 13½" FLUES"; "¾" ROD GRATE FULL WIDTH OF
  FIRE BOX".
- Exit: flues 9" × 4½" into a "FLUE COLLECTION BOX" 9" wide; passive air inlet and damper in the
  chimney.
- Chimney: 13½" × 13½" "past top of arch", "TAPER IN" to 9" × 9" at the top; "CHIMNEY HEIGHT MIN 10'
  MAX 12'".
- Salt: four salt holes, in the door, top and back (p.128). The back usually fires cold, so a side
  burner is lit or wood stoked there (p.128).
- Door: "24" (+-) DOOR" in the side wall.
- **Not given:** arch rise and thickness; firebox length and grate height; ash pit; frame; firing time.

### `olsen-first-kiln`: Olsen's first kiln, Col Levy's pottery, Australia, November 1963

- Pages: p.126 (text); p.127 (text).
- John Chappell's salt-kiln design, built with second-hand bricks and the cheapest fireplace bricks;
  "mistakes were made in the depth of the firebox" (p.126). Fired with free crankcase oil and stoked
  with wood, for his first all-salt-glaze exhibition (p.127).
- **Not given:** any dimension (see `bowen-mountain` for the revised design).

---

## 5. Chamber and climbing kilns

### `hotchkiss-raw-clay`: six-chamber raw-clay kiln, 1971

- Pages: p.33 (text); pp.54–56 (text, Figs 2-39 to 2-45); p.57 (text, Figs 2-46 to 2-49).
- Builders: Richard Hotchkiss and a workshop group, 1971. One note lists Rimas VisGirda among the
  builders; the other credits him with the photos. Still fired by Richard Hotchkiss and Tom Orr
  (p.57). Place not stated; the brick clay is from Lincoln, California (p.54).
- Fuel: not named. Captions "Firebox firing, May '97" and "Side stoking of the upper chambers, one
  chamber at a time" (p.57) point to a solid fuel, almost certainly wood (?).
- Draft: climbing chamber kiln, six chambers on a slope, chamber 6 the uppermost.
- Cone and firing time: not given. Fire the first firing slowly or the raw blocks blow out (p.57).
- Chambers: "average chamber (5 x 5 x 6ft) 150 x 150 x 180cm tall" (p.56). Whether these are inside
  sizes, and whether 6 ft is to the crown, isn't said. 150 ft³ each, about 900 ft³ in all (derived).
- Bricks (p.54): raw (unfired) blocks of 50 % Lincoln 60 fireclay and 50 % coarse sand, cut from a
  trough mould with a wire: 9 × 10 × 18 in (23 × 25 × 46 cm); 9 × 10 × 9 in (23 × 25 × 23 cm);
  9 × 5 × 5 in (23 × 12.5 × 12.5 cm).
- Mortar: 50 % Lincoln fire clay, 50 % sand, plenty of it, soft (p.33, p.55).
- Arches (pp.55–56): front and back walls built first, then an arch form; blocks shaped with an axe,
  key row included; each arch roped until the arch below was finished to buttress it. The photos show
  near-semicircular arches. Span, rise and thickness not given.
- Walls: side walls filled in last, with a door on one side and stoke and spy holes on both sides
  (p.56); pointed-arch stoke hole (Fig 2-44). Thickness not given.
- Inlet flues: "flue holes" in the straight wall (Fig 2-40); count and size not given.
- Firebox: domed, with bracing round it (Fig 2-46).
- Chimney: commercial firebrick to 12 ft (3.6 m), then 18 ft (5.5 m) of scavenged hydraulic water
  pipe (pp.56–57). About 30 ft in all (derived).
- Building order: chamber 6 first, downward; each chamber dried with a fire as finished; the top two
  bisque-fired before the rest were finished (pp.55–56).
- Steel: none mentioned; rope braces during building only.
- Service: still firing after 30 years (p.33).
- **Not given:** fuel; inside sizes; slope; wall thickness; arch span, rise, thickness; flue sizes;
  firebox size; chimney section; cone; firing time.

### `kyoto-climbing`: Kyoto-style climbing chamber kilns (type)

- Pages: pp.89–94 (text, Figs 4-21 to 4-34); p.96 (text); p.205 (text, Fig 8-16).
- Hundreds in south-east Kyoto, each fired every fortnight (p.89). From the early 1960s wood grew
  scarce; smog ordinances moved Kyomizu, Gojo and Sennyuji to electric or gas, ending almost 600
  years of climbing kilns in Kyoto City (p.90).
- Fuel: wood. Draft: cross-draft chambers, climbing.
- Chamber: "Kyoto climbing kiln dimensions: 6–7' tall, 4.5–6' wide" (Fig 4-28). Fig 4-31: a Kyoto
  chamber 4' wide × 6' tall (pointed arch) against "other climbing kilns" 6' wide × 6' tall.
- Arches: reduction chambers have a double-radius arch, its peak set toward the back (Fig 4-32);
  middle-fire and oxidation chambers a nearly single-radius arch (pp.91–92).
- Flues (Fig 4-28): outlet "approx. 9 x 5" spaced 9" apart"; inlet "9 x 6" – 9 x 4.5""; a mark "18""
  inside the chamber at the outlet flue (meaning unclear (?)). Standard 4½ × 9 in flues spaced 9 in
  apart can be used instead (p.96).
- Chamber firebox (himae): a 9 in (23 cm) trough next to the front wall with one row of empty saggars
  as the bag wall, stoked through the takaguchi (p.92, Fig 4-34). With saggar settings and no sunken
  firebox, channel bricks lie along the floor 9 in (23 cm) apart between the settings and the front
  wall, the space at least 9 in, up the full height of the stacking (p.205).
- Stoking: both sides at once; floor zones hana, tsunaka, donaka by the length of the toss (Fig 4-33);
  upper half nibon is the main stacking, lower half ne (p.93).
- **Not given:** chamber depth; wall thickness; step between chambers; main firebox (dogi) size;
  chimney; cone.

### `kyomizu`: Kyomizu climbing kiln, Kyoto

- Pages: pp.89–91 (captions, Figs 4-23, 4-25 to 4-27, 4-29, 4-30).
- Olsen fired it every month for 2½ years (Fig 4-23), its 5th chamber in 1962 (Fig 4-26). Fig 4-27:
  chambers numbered 1 to 10 (a break between 4 and 10), "4' INSIDE" (?) over chamber 3. The second
  chamber was for reduction only (Fig 4-30). Wood; climbing.
- **Not given:** any reliable dimension.

### `tobe`: Tobe Village kiln, Shikoku

- Pages: p.90 (text); p.92 (text).
- The largest chamber kiln; destroyed July 1963. Total capacity 15,000 ft³ (425 m³); seven chambers;
  the largest chamber 25 ft (7.6 m) long × 10 ft (3 m) tall × 10 ft (3 m) wide (p.90). "Required 40
  tons of wood to fire": the sentence reads as the largest chamber but may mean the whole kiln.
- Chamber width almost equal to its height, so more oxidizing and harder to reduce (p.92). Wood;
  climbing.
- **Not given:** the other chambers' sizes; walls; flues; firebox; chimney; slope; cone; time.

### `onda-koishibara`: Onda and Koishibara kilns, Kyushu

- Page: p.92 (text). Chamber width almost equal to height, like Tobe.
- **Not given:** any number.

### `suzuki-kyoto`: Suzuki cooperative kiln, Torincho Street, Kyoto

- Pages: p.93 (text); Fig 4-35 (site plan).
- Fuel: wood bundles. Draft: climbing, seven chambers.
- Cone and time: approximately 56 hours to cone 8–9 (text). By chamber (Fig 4-35): 1 and 2 cone 10
  reduction; 3 cone 8–9 reduction and oxidation; 4, 5, 6 cone 8–9 oxidation; 7 "bisque high Δ1"
  (cone 1 (?)).
- Chamber: "14 x 6 1/2 x 4 1/2 ft (4.3 x 2 x 1.4m)" (the first figures, lost in the gutter in the
  scan, read by the user, 2026-10-29). Read by the Kyoto
  proportions as 4.3 m across × 2 m tall × 1.4 m deep (the note's interpretation); about 425 ft³ per
  chamber (derived).
- Stoking: firebox 15 hours to 1832 °F (1000 °C); then each chamber's sides. A bundle is 15 in /
  38 cm across (the inches washed out at the gutter; the printed 38 cm ÷ 2.54 = 14.96 in agrees;
  Checked on the page image, p.93, 2026-10-30) × 18 in / 46 cm long. ¼ bundle per stoking in hour 1, ½ in hour 2, ¾ in hour 3; from
  hour 4 one bundle every 3–4 minutes (reducing); up to two bundles per stoking in hour 7. Chambers
  1–3: about 75 bundles per side, 7 hours (reduction). Chambers 4–7: [number lost] bundles per side,
  5 hours (oxidation).
- **Not given:** walls; flues; firebox size; step; chimney.

### `bidai`: Kyoto Bidai climbing kiln, 1962

- Pages: pp.94–97 (text, Figs 4-36 to 4-43); pp.200–201 (text, Figs 8-5 to 8-7).
- Built 1962 (p.97), its foundation dug into a small slope. Fuel: wood. Draft: climbing cross-draft;
  firebox, three chambers, chimney. Cone and time: not given.
- Overall: 19' 5" long; "3 TO 1 SLOPE" (about 18°, derived) (Fig 4-36).
- Foundation: blocks 7 in/18 cm deep × 11 in/28 cm long × 9 in/23 cm wide; the whole perimeter wall
  (chimney included, firebox not) built up to the start of the arch curve (p.94).
- Bricks: 6 × 3½ × 9½ in (15 × 9 × 24 cm) to 6 × 6 × 9½ in (15 × 15 × 24 cm), thick fireclay joints;
  tatami arch bricks "6 x ?" (Fig 4-37; the rest washed out at 600 dpi, 2026-10-31).
- Front wall: leans slightly in to 38 in (97 cm), where the arch begins (pp.94–95, Fig 4-37).
- Chambers (Fig 4-36, drawing): inside width 73"; depths 42", 46", 36"; floor to crown 59", 65", 59";
  arch thickness 9". In chamber 2 a "56"" mark, from the floor to the
  underside of the round hole in the arch, drawn like chamber 1's "SPYHOLE" (Checked on the page
  image, 2026-10-31). Doors 20" wide,
  one per chamber, all on one side. Middle-chamber stoke hole (aizashiguchi) 15" above the floor.
  Vapour holes in rows; spy holes. Bounding volumes about 105, 126 and 90 ft³, about 321 ft³ (derived;
  the arches make it less).
- Walls between: "6" × 12"" (firebox to chamber 1) and "7" × 12"" (chamber 1 to 2), hatched as
  masonry: probably pier or flue sizes (?). A 15" wall at the back of chamber 2 with 12" flue openings
  above it; a 12" step and a 12" exit flue at the back of chamber 3.
- Arches (p.95): the peak set back from the chamber centre line to throw the thrust onto the common
  wall and on to the chimney; the first chamber wall braced while arching; arches wedged from the
  springing to the top on both sides.
- Overcoat: 3 in (7.5 cm) of fireclay, dirt and straw, with the vapour- and flame-hole sticks left in
  to burn out (p.95).
- Firebox, Fig 4-36 (drawing): semicircular front with a slotted wall; mouth 9" wide × 18" deep; 28"
  from the mouth to three pointed flame-diffusing blocks at the chamber entrance; 46" long overall
  with an 18" ash-pit section; heights 18" (the ground to the 9" slab over the ash pit) and 40"
  (the ground to the top of the front, where its arch starts), both Checked on the page image,
  2026-10-31; a 9" slab at grate level; dirt floor rising to the first chamber, whose floor is 42" above
  the ground at the front. Built without an arch form, after the chambers (p.95). Four flue openings
  show at the top of the firebox wall (photos, Figs 4-42, 4-43).
- Firebox, Fig 8-7 (drawing, p.201): wall 9½–10" thick; six fireclay grate bars; grate zone 14"; 26"
  from the grate to the first chamber's wall; air and stoke opening 12–14"; ash-pit arc 26"; outer
  arc "?3"" (digit lost); six flues into chamber 1, the middle three deflecting the flames; flue
  spacing printed "73"" (?), about 7 in by scale (**Flagged**). Side: 40" overall (?); 18" on the air
  side; ash pit 14" high; stoking opening 14"; retaining wall and grate rest 20"; 42" from the
  foundation to the flue; flue 12"; 40" of upright wall round the firebox before it arches over.
  Text p.200: the firebox slopes from the entrance along the wall and up to the corner flues; the
  ash pit runs to the first chamber's inlet flues; the retaining wall holds the earth mound and
  carries the grate-bar rests; arched with tatami bricks. For a larger kiln, enlarge the firebox in
  proportion (p.201).
- The two firebox drawings differ: length 46" (Fig 4-36) against 40" (?) (Fig 8-7); mouth 9" wide
  against a 12–14" opening; four flue openings (photo) against six flues (Fig 8-7). They may measure
  different things; neither note resolves it.
- Chimney (Fig 4-36): chimney flue 9" × 9"; flue channel 18" deep behind chamber 3; chimney wall 9";
  heights 73" (ground to the base of the chimney section), 41" above that and 9" (top course), as
  drawn. In plan the chimney spans the full 73" width as a grid of flue channels. No total height is
  printed (73 + 41 + 9 = 123 in, derived, if the three are stacked).
- Flues: odd local bricks explain the odd flue sizes; standard 4½ × 9 in (11½ × 23 cm) flues at 9 in
  (23 cm) can be used (p.96).
- **Not given:** side-wall thickness; flue sizes and counts between chambers (other than the 12"
  openings); total chimney height; damper; cone; firing time.

### `kawaii`: Takichi Kawaii's kiln, outside Kyoto, 1984

- Pages: pp.96–97 (text, Figs 4-44 to 4-48); p.200 (text).
- Takichi Kawaii (1908–89). Built spring 1984; Kyoto style; four chambers; its floor plan "almost
  exactly" the Bidai kiln's (p.97). Fuel: wood. Draft: climbing cross-draft. Cone and time: not
  given.
- Chamber: 7 ft wide × 4 ft deep × 5 ft 8 in tall (213 cm wide, 122 cm [deep], 173 cm tall). About
  159 ft³ bounding per chamber, 635 ft³ for four (derived).
- Flues: inlet and exit 7 × 10 in (18 × [25] cm); the last chamber's exit flues 9 × 10 in
  (23 × [25] cm); exit flues the same in each chamber (Fig 4-48); the chimney's flues are a row of
  openings between brick piers (Fig 4-47).
- Step: 12 to 15 in between chambers, printed "(30.5 x 38cm)" (**Flagged**: 30.5 to 38 cm).
- Firebox (dogi): 5 ft (152 cm) tall; [grate (?)] bars 18 to 24 in (46 to 61 cm) long, spanning the
  ash pit onto the firebox mound; [two (?)] extra stoke holes on its sides (p.97). The same firebox
  as the Bidai kiln (p.200).
- Arches: tatami-mat bricks in the arches and the firebox; bracing on the dogi and the front chamber
  against the thrust, "a must" on such kilns (p.97). Earth-mix plaster outside; a stoke hole built
  into each door's bricking (Fig 4-46).
- **Not given:** chimney; walls; arch thickness; slope; cone; firing time.

### `fujiwara-bizen`: Kei Fujiwara's Bizen kiln, Imbe, Okayama

- Pages: pp.98–104 (text, Figs 4-49 to 4-61); p.105 (text). The heading prints "FUGIWARA", the
  captions "Fujiwara". Olsen visited in 1984 (p.105).
- Fuel: wood (sticks, split logs, fireplace logs, pine needles). Draft: climbing cross-draft, with a
  deliberately low chamber draft for the most ash.
- Cone: not given; saggar cones at the spy holes, but fire colour usually decides (p.104).
- Firing: exactly seven days: 2½ days stoking the fire-mouth air duct (pre-heating), 4 days stoking
  the fire mouth from the fire hole, 12 hours stoking the chambers; temperature reached at 6½ days,
  then a soaking fire to finish the first chamber and the kedo (pp.103–104). Then all spy holes and
  dampers are closed tight and the kiln cools very slowly, over about three days (p.105).
- Spaces in order: dogi (fire mouth, the first and most important chamber; a gradual incline stepped
  halfway, the steps being shelves across its width) → himitsu (a "secret" chamber in a 24 in
  (61 cm) draft flue) → first chamber (ichi no ma, the largest) → kedo (second chamber, much lower and
  [narrower]) → flue stack → chimney (pp.99–101).
- Plan, Fig 4-53 (drawing): dogi 8' long, 10' wide inside; "12"" (first flue wall, about seven flue
  openings) and "11"" (the himitsu); second flue wall; first chamber 4'6" long, the widest part (its
  width arrow unlabelled); flue wall; kedo 2'10" long; last flue wall; 3'6" to a round chimney
  centred at the back.
- Heights, Fig 4-55 (drawing): dogi 9' (Checked on the page image, p.101, 2026-10-31), himitsu 2', first chamber 5', kedo 4', chimney 25';
  slope 5" rise in 12" run (about 22.6°, derived).
- Himitsu, Fig 4-52 (drawing): 2' tall; "14"" (upper) and "10"" (lower) inside; "2'" at the dogi-side
  wall face (meaning unclear); entrance flue at floor level from the dogi, exit flue higher into the
  first chamber.
- Flues (pp.100–101): into the himitsu very small, 3 × 6 in (7.5 × 15 cm), to raise the draft; himitsu
  to first chamber on average 6 × 9 in (15 × 23 cm), with no rise between the himitsu's entrance and
  exit flue levels; first chamber to kedo [6 x] 9 in (15 × 23 cm); kedo exit flues 6 × 10 in
  (15 × 25 cm) into a stack that runs 3½ ft (107 cm) before rising into the chimney.
- Steps: a rise of 5 in (12.5 cm) for every 12 in (30.5 cm) between chambers; no rise between the
  kedo and the chimney (p.101).
- Walls: 10 to 13 in (25 to 33 cm), tightly built, no vapour holes, an overcoat of fireclay, straw
  and earth (p.100). No expansion joints: the long, slow firing and cooling take the movement.
- Chimney: about three times the kiln's total rise, 25 ft (7.6 m); the flue stack enters it through
  a 10 in (25 cm) diameter opening, the same as the kedo exit flues' height; damper at that entrance
  (p.101).
- Fire mouth: the fire-mouth hole is 3½ × 2 ft (107 × 61 cm) when open (p.102); dogi door with a fire
  hole (Fig 4-55); mempo ana stoke holes and spy holes low in the dogi.
- Side fire holes (takiguchi) in the first chamber: p.100 says "side fire holes"; p.104 says they are
  on one side of the kiln only.
- Stacking (pp.102–103): the dogi on three step levels; 3 × 5 in (7.5 × 12.5 cm) under-draft spaces
  across the floor under each step's setting; 15 cm (6 in) between the top setter and the roof; first
  chamber shelves to within 6 in (15 cm) of the top, with a 9 to 10 in himichi trough in front for
  the takiguchi; kedo pots piled about two-thirds full.
- Wood (pp.103–104): air-duct sticks 12 to 15 in (30.5 to 38 cm) long, 1 to 3 in (2.5 to 7.6 cm)
  thick; fire-mouth split logs 3 to 4 ft (91 to 122 cm) long, 2 to 5 in (5 to 12.5 cm) thick; chamber
  wood 12 to 15 in × 1 to 2 in, thrown in until a 12 in (30.5 cm) flame shows at the spy hole.
- Ware loss: about 50 % with the artist's clay, about 20 % with commercial Bizen clay (p.99).
- **Not given:** first chamber and kedo widths; arch shapes and thicknesses; chimney section (only the
  10 in entry); damper size; cone.

### `kanayama-bizen`: commercial Bizen chamber kilns; Kanayama Pottery

- Pages: p.99 (text); p.105 (text, Fig 4-62); p.106 (text, Figs 4-64 to 4-66A).
- Commercial Bizen ware is fired in "ordinary" climbing chamber kilns (p.99, p.105). At the Kanayama
  Pottery (Ryoji Matsu…, name cut off) the chamber doors are bricked up in a pattern that lets
  charcoal in at every shelf level; a long push shovel, as long as the chamber, drops charcoal on the
  ware at final temperature; then the chamber is closed tight. Charcoal ports above the ware in the
  back wall (Fig 4-65). Wood, with charcoal at the end.
- **Not given:** any dimension.

### `chappell-domura`: John Chappell's Domura tandem kiln, Japan

- Pages: p.33 (text); p.126 (text, Figs 4-148 to 4-151); p.243 (text).
- Builder: John Chappell, Domura (printed "[D?]omura" on p.33). p.126 dates the kiln 1962; p.243 says
  Olsen and Chappell fired the salt-glaze kiln in 1963.
- Fuel: wood (two fireboxes drawn); p.243 doesn't name it. Salt glaze in one kiln. Draft: cross-draft.
- Volumes (p.126): a two-chamber kiln, each chamber 40 ft³ (1.13 m³), and a salt-glaze kiln of 50 ft³
  (1.42 m³), separated by a common wall and sharing one chimney.
- Plan, Fig 4-149 (drawing): salt chamber 3' wide × 5' long, "3' TALL", "(9" WALLS)", its firebox "30"
  below floor". Chamber kiln: first chamber 4' wide, 31" long, firebox 9" (across the kiln) "12"
  below floor", an 18" opening in the side wall; second chamber 31" long, "5½' TALL" (? first digit
  partly cut). A 9" dimension at the common wall and at the exit flues; "18-12" SHELVES used in
  chamber kiln"; draft hole; collection box.
- **Flagged**: 4' × 31" × 5½' is about 57 ft³ and 3' × 5' × 3' is 45 ft³ (derived), against the
  printed 40 and 50 ft³.
- Chimney: "CHIMNEY 12 X 12" tapering to 9 X 9" 25' TALL" (Fig 4-149).
- Materials: intermediate-duty fire-clay brick in a mortar of 2 parts sand, 2 parts [grog (?)]
  (stoneware), 1 part stoneware clay (p.33). Foundation of concrete blocks, then common red brick, then
  medium-duty firebrick (p.126, Fig 4-148).
- A long, low chamber is excellent for salt: salt goes straight in above the ware (p.126).
- Shed (p.243): a corrugated plastic roof; halfway through salting, flame leaked through the arch,
  door and salt ports, and the roof melted, sagged toward the arch and caught fire.
- **Not given:** first-chamber height; arch shapes; firebox lengths and grates; flue sizes; damper;
  cone; firing time.

### `olsen-chamber-p23`: Olsen's chamber kiln

- Pages: p.23 (text); p.47 (text).
- Shelves: square-edge fire tiles 30.5 × 46 × 5 cm (12 × 18 × 2 in) (p.23). Its ring arch opened
  almost ½ in (1.3 cm) in firing (p.47).
- **Not given:** everything else. It may be `olsen-two-chamber`; the book doesn't say.

### `olsen-two-chamber`: Olsen's two-chamber wood kiln, side-stoked

- Pages: p.202 (text, photos Figs 8-8 to 8-10); p.203 (captions); p.206 (text, Fig 8-17).
- Fuel: wood. Draft: not stated. Cone and time: not given.
- First chamber: 55" wide, 48" tall, 8' long (Fig 8-17). The roof shape, and whether 48" is to the
  springline or crown, aren't given. 147 ft³ as a box (derived).
- First-chamber firebox (p.202): a side firebox 18 in (46 cm) below the first chamber's floor; a
  fast-fire-style metal grate 9 in (23 cm) tall, the chamber's width and depth; air along the front
  wall, which is the primary air while the space under the stoke hole is closed; ash pit 15 in
  (38 cm) deep. Close the front at the end so the chamber cools slowly.
- Wall between chambers: 9" (drawing). Flue hole into the second chamber: 15" wide × 20" tall, the
  grate at half its height (drawing).
- Second-chamber firebox (p.206, Fig 8-17): sunken ash pit under the inlet flue, the grate bisecting
  the flue; firebox 14" wide; ash pit 15" deep; grate bars ¾" apart; stoke hole 7" × 7". An air tube
  across the chamber under the grate: a 5 in (12.5 cm) extruded square tube with perforated sides,
  smaller holes near the supply end and larger at the far end, with a shutter outside.
- Identity: the same air tube (5 in, graduated holes, under the grate), ¾ in grate bars, an 8'
  chamber and a 55" dimension also appear in `hollyweird` (pp.116–117). It may be the same kiln; the
  book doesn't say.
- **Not given:** second-chamber size; roof; walls; exit flues; chimney.

### `olsen-three-chamber`: Olsen's three-chamber climbing kiln

- Page: p.224 (text).
- Fuel: gas, not named. The burners are Eclipse compound injectors, which the same page says are for
  1200–3300 BTU/ft³ gas (LP). Draft: climbing.
- Chambers: three, each 120 ft³ (3.4 m³). 360 ft³ in all (derived).
- Burners: six Eclipse 2 in (5 cm) compound injectors, model TR-80, about 214,200 BTU/hr each at
  10 in. WC on a No. 18 orifice; total at peak 1,285,200 BTU/hr. The note's check against Table 8-7:
  a #18 at 10 in. WC gives about 211,700 BTU/hr on butane and 191,000 on propane, about 118,000 on
  natural gas, so the rating fits LP.
- **Not given:** where the burners are; chamber dimensions; walls; flues; chimney; slope; cone.

### `kitade-tojilo`: Kitade Tojilo chamber kiln, Kutani, Japan

- Pages: p.202 (text, Fig 8-11); p.203 (caption, "modern chamber-kiln firebox"). The note matches
  Fig 8-11 to this kiln by its content.
- Fuel: wood, long slabs. Draft: chamber (climbing); "slope 33%" (drawing).
- Chamber: 4' wide, 5' tall, 8' deep; arched (drawing). 160 ft³ as a box (derived).
- Firebox (text): side-stoked; slab wood on a grate the full width of the chamber; a deep ash pit
  under wide-spaced grate bars; air from two openings at the bottom of the front wall.
- Firebox (drawing): 15" wide inside; 42" from the bottom to the sloping roof, which slopes 30°; ash
  pit 24" below the grate; 12" from the grate to the flue-inlet sill; flue inlet 9" × 12"; another
  12" on the chamber side, from the flue-inlet sill's level up to a level line beside the flue's top
  (what that line is isn't labelled); stoke hole 9" × 7"; fireclay grate bars at 6" spacing; two "air draft &
  ash pit holes" in the front, each 12" wide × 18" tall; "2½"" from the end wall to a line through the
  first hole (printed with an inch mark, but about 20 in when scaled against the 12" hole, derived:
  **Flagged**); "10" on two base
  edges, unit not given. The 12" and 2½" were Checked on the page image, 2026-10-31.
- Olsen's critique: more, smaller air holes spread across the chamber; grate bars at minimum spacing;
  grate-level mouse holes.
- **Not given:** number of chambers; walls; arch; exit flues; chimney; cone.

### `blakebrough-sturt`: Les Blakebrough's kiln, Sturt Pottery, Mittagong, Australia

- Pages: p.205 (text, Fig 8-15); p.208 (text, Fig 8-21 photo).
- Fuel: wood in the chamber firebox; also an oil-drip system with six drip channels (p.208). Draft:
  chamber kiln. Not the Tasmanian fibre kiln (`blakebrough-tasmania`).
- First chamber: 6' tall, 45" wide, 6' deep; arched (drawing). 135 ft³ as a box (derived).
- Chamber firebox: a channel across the full width of the "6 ft chamber" (text); 12" tall, 9" wide,
  6' deep (drawing); grate bars or long soaps wedged along the wall and floor on 9 in (23 cm) centres;
  ash drops to the channel bottom; coals raked with a long hooked poker through the stoke hole.
- Inlet flues 9" × 4½"; stoke hole in the side; a 12" × 19" kiln shelf drawn.
- Wood: 1 × 1 in (2.5 cm) to 2 × 2 in (5 cm) thick, 18–24 in (46–61 cm) long.
- **Not given:** number of chambers; main firebox; walls; arch; exit flues; chimney; cone.

---

## 6. Tube, groundhog and tunnel kilns

### `anagama-hole`: anagama dug into a clay hill (type)

- Pages: pp.83–84 (text, Figs 4-2 to 4-5). The photos (Figs 4-3, 4-4A, 4-4B) don't name a place.
- Fuel: wood. Draft: cross-draft, single-chamber tube.
- How built (text): a cavity dug into a clay bank, widened, then tapered back into a chimney flue to
  the surface; firebox, floor and walls shaped in the clay; a fire of rising intensity for weeks
  bisqued the walls into a monolith.
- Fig 4-5 (drawing): entrance and firebox 2' × 2'; chamber height 3½' (? fraction faint), width 5¼',
  length 9–12'; "slope angle 25" (degrees); walls "ground clay bisque"; a vertical chimney flue at the
  back up to the hill's surface.
- **Not given:** chimney height and section; flues; temperature; firing time.

### `tamba`: Tamba tube kilns, Tachikui, Japan

- Pages: pp.85–88 (text, Figs 4-6 to 4-20A); p.210 (text).
- 23 kilns, protected as cultural properties; built in the early Kamakura period, printed
  "(1185–1392)" (**Flagged**: Kamakura ended 1333), by migrant Korean potters; unchanged for 650
  years (p.85; the 650 Checked on the page image, 2026-10-31; the word before it is lost in the
  gutter, so "about", "over" or "for" can't be told).
- Fuel: wood, side-stoked with split kindling. "Today a majority" fire the firebox with an oil burner
  and blower (p.86); preheated and fired with Denver-type oil burners (p.210). Draft: climbing tube,
  cross-draft.
- Size: an anagama extended to approximately 120 ft (36.5 m), half above ground (p.85). Fig 4-7: "6–8
  door segments. Kilns are 120–150" long" (the inch mark must mean feet: **Flagged**); stoke holes
  1½ ft apart (read by the user, 2026-10-31; earlier read 2½').
- Load: pots 13–24 in (33–61 cm) tall, up to 500 a firing, no shelves; saggar setters level them
  (p.85–86).
- Firebox (dogi): 6 ft (183 cm) deep and 5 ft (152 cm) across at the entrance flues (p.86). Fig 4-16:
  firebox 6' long; 4' vertical, from the ground line to the first chamber's floor; first chamber
  3½' tall (both Checked on the page image, p.87, 2026-10-31).
- Flues (drawing): firebox flue holes "9 x 18"", four arched openings (Fig 4-13); chamber flue holes
  "20 x 12"" and "24 x 12"", middle and last chamber, which is which uncertain (Fig 4-12).
- Firing (pp.86–87): firebox stoked about 36 hours, bringing the first three or four stoke holes to
  about 1832 °F (1000 °C); then side stoking, leaving a 9 in himichi fire channel every second or
  third stoke hole; 14 to 18 hours (read by the user, 2026-10-31) and about 200 bundles (15 × 15 × 30 in / 38 × 38 × 76 cm) of
  kindling; at the end the flues plugged and the firebox sealed. The front is unloaded within half a
  day (pp.87–88).
- End chamber: bisque only, with "chimney open holes" (Figs 4-18, 4-19).
- Doors: arched, bricked up for firing; "supporting wall in front of all doors" (Fig 4-15; its sizes
  unreadable).
- Tatami bricks (Fig 4-6, p.85, Read on the page image 2026-10-30): "The tube kiln construction and
  Tatami bricks. The bricks are made by being rolled in a Tatami mat"; the drawing's label: "Hand made
  by rolling in Tatami mat". The drawing shows a rolled brick narrower at one end than the other,
  conical (the user's reading, 2026-10-30), with a hole along its axis, laid in courses round the
  tube's arch. No sizes, taper, clay or firing given.
- **Not given:** tube width and height (except the first chamber's 3½'); slope; walls; chimney;
  tatami brick sizes.

### `bae-gilgama`: Mr Bae's Korean gilgama (Silla Dynasty type), NCECA

- Pages: p.107 (text, faded; Figs 4-67 to 4-69); p.108 (text, Figs 4-70 to 4-74).
- Builder: Mr Bae, a third-generation Onggi potter, for an NCECA conference (year not given).
- Fuel: wood, slab wood 3–5 ft (91–152 cm) long. Draft: cross-draft, climbing. Fired to temperature,
  then sealed for black (carbonized) ware.
- Shape: bricked up in a teardrop form, butting into the back wall (p.107).
- Slope: "A 20% slope was used, which is standard for most kilns of this style" (p.108); Fig 4-67
  prints "20° SLOPE". **Flagged**: 20 % is about 11.3°, 20° about 36 %.
- Fig 4-67 (drawing): length 16' along the base; chamber marks "4'" and "6'": the 6' arrow runs from the
  front of the floor to the back wall, the 4' arrow across it (Checked on the page image,
  2026-10-31; the width is not given elsewhere); height to the tallest point "4½" (?, read as 4½ ft); front "18"" (?, the step or the
  mouth) and "4'" (combustion area depth (?)); "COMBUSTION AREA", "NO GRATES"; wood laid at 22° (?).
- Floor: an 18 in (46 cm) step, then the chamber floor slopes up (p.108).
- Exit flues: two, 4½ × 9 in (11.5 × 23 cm), in the back wall (p.108; drawing "9"", "EXIT 4½"").
- Chimney: 8' high to the ground line; "DAMPER ON TOP" (drawing).
- Sealing (p.108): stuff the firebox with wood, brick and dirt-seal the door, close and cover the
  flues, find leaks with burning newspaper and mud them.
- **Not given:** width; walls; chimney section; cone; firing time.

### `la-borne`: La Borne tunnel kilns, France

- Pages: p.109 (text, blurred; Fig 4-78); p.110 (text, Figs 4-79, 4-80); p.111 (text).
- Fuel: wood (split oak and birch, then branches). Draft: tunnel (cross-draft) on a slope, fired only
  from the firebox at the low end; exit at the high back end.
- Size: "The La Borne tunnel kilns ranged in size from 1766 to 2825 cu. ft (50 to 80 cu. m)" (p.109).
- Plan, Fig 4-78 (drawing, blurred): 10' wide at the bag wall, 12' at the widest; 27' from the bag
  wall to the back; firebox "4'" long with a grate; back door. "The whole end of the kiln can be left
  open and closed by bricking."
- Elevation, Fig 4-78 (blurred): "ABOUT 1:9 SLOPE" (the digit read by the user, 2026-10-29: about
  6.3°, derived); skewback line "7'?";
  a "6'" (?) height near the bag wall; a "24'" (?) mark; stoke opening above the grate, air inlet and
  ash pit below; back entrance door "3'" or "5'" (?); spy holes, flue-control holes and exit flues at
  the back.
- Back: ware goes in through the back; bricked up, that entrance is also the exit flue (p.109). Since
  the kiln's "rebirth", two chimneys stand one each side of the back door (p.110).
- Firebox (p.110): "quite large". Grate usually a bonded arch with nine holes per row, each "5 x 5 x 5
  x 7in. (12.5 x 12.5 x 12.5 x 18cm)", or ring arches 4½ in (11.5 cm) apart (Fig 4-80). A space about
  2 ft (61 cm) wide between the grate and the bag wall, for preheated air and raking.
- Bag wall: greenware bricks in a checkerboard, the gaps acting as inlet flues, leant away from the
  flame, rebuilt after each firing (p.110).
- Floor: calcined dirt in tiers for saggars (p.110).
- Temperatures (p.111): about 2372 °F (1300 °C) by the firebox, [2192 °F] (1200 °C) in the middle,
  about 2012 °F (1100 °C) at the rear; ware graded by thirds.
- Firing (p.111): preheat ("driving out") 2½ to 3 days; *le petit feu*, up to four days; *le grand
  feu*, about one day, with light salting near the end. About 7–8 days (derived).
- **Not given:** heights (except "6'" (?)); slope; walls; flue and chimney sizes.

### `groundhog-basic`: groundhog kiln, "basic groundhog dimensions" (type)

- Pages: p.111 (Fig 4-85); p.112 (text).
- Fuel: wood. Draft: cross-draft: full-width firebox at one end, full-width chimney at the other.
- Chamber (text p.112): "Average chamber 29 to 48 in" high, "7 to 10 ft" wide and "12 to 24 ft (3.7 to
  7.4 m) long"; like a cylinder sliced lengthwise at or slightly off the centre, the smaller part laid
  down. The metric pairs print as products ("(73.5 x 122cm)", "(213 x 305cm)"): **Flagged**, ranges
  are meant.
- Fig 4-85 (drawing): firebox width 5–10'; shallow firebox about 4–6' (?) long; "12–15" RISE FROM
  SHALLOW FIREBOX"; or a "DUGOUT FIREBOX", "42–48" DEEP"; "10–20' WARE PLATFORM"; floor to crown
  29–48"; chimney inside 9–30" wide; chimney 5–12' tall; six exit flues drawn at the chimney wall.
- Proportions (p.112): one third firebox to two thirds ware platform (shallow firebox), to one quarter
  firebox and three quarters platform (dug-out firebox).
- Chimney: 5 to 10 ft (152 to 305 cm) by size and length (p.112); the drawing prints 5–12'. Dug-out
  fireboxes (about 48 in / 122 cm deep) allow shorter chimneys.
- Building: dug into the ground (earth buttress, dirt cover) or on the ground with rock or other
  bracing. Shallow-firebox kilns usually load from the front, dug-out ones from the chimney end.
- **Not given:** wall and arch thickness; exit flue size; chimney section beyond the 9–30" width.

### `meaders-cheever`: Cheever Meaders's groundhog, Cleveland (Mossy Creek), Georgia

- Pages: p.112 (Figs 4-86 to 4-89); p.113 (text).
- Fuel: wood. Draft: cross-draft, shallow-firebox groundhog. His last kiln (Fig 4-87).
- Fig 4-89 (drawing, view from the chimney end): floor to crown 48"; a central T-shaped post, 30"
  from the floor to the underside of its top; "FLUE HOLES – 5 x 9 – TOTAL 6" in the back wall;
  "18"–20"" along the flue row; width 5' across the base at that end (the 30", 18"–20" and 5'
  Checked on the page image, 2026-10-31); length 12' along the arch; walls "RUBBLE BRICK"; chimney top 9" × 5'
  (p.112, read by the user, 2026-10-31; the scan's "2'" and "1'" were misread at the page edge).
- **Not given:** firebox; full width (if 5' isn't it); chimney height; wall thickness.

### `hart-square`: Hart Square groundhog, Vale, North Carolina, 1987

- Pages: p.112 (captions, Figs 4-89 [sic] to 4-93); p.113 (text, drawing "NOT TO SCALE", illegible).
- Builder: Kim Ellington, 1987. Wood; dug-out firebox; front stoke holes.
- Construction (p.113): bricks laid over a form of arch boards on slat runners (Ellington used the
  boards from Burlon Craig's kiln of the early 1930s). The arch meets the chimney as a full arc, the
  chimney's front wall built on it, carried by two 9 × 9 in (23 × 23 cm) columns 18 in (46 cm) in
  from the sides; the gap between them, about 66 in (168 cm), is the entry to the ware chamber. So the
  chamber is about 10 ft (120 in) wide at the chimney (derived).
- Performance (p.113): cool along the rear side walls (ware there didn't vitrify, so it was used for
  flowerpots). Olsen's fix: equally spaced exit flues along the back wall, brick up the entry with
  flues in it, and a centre damper above the chimney door.
- Drawing: a firebox "?5" DEEP" label (35" or 3'5" (?)); nothing else readable.
- **Not given:** length; height; firebox; flues; chimney height. Can't be modelled.

### `ellington-new-hog`: Kim Ellington's "new hog"

- Pages: p.114 (text, Figs 4-95 to 4-100); p.115 (photos, Figs 4-101 to 4-104).
- Fuel: wood, stoked from the front and through side stoke holes; salted at the back through the
  side stokes. Draft: cross-draft (groundhog).
- Plan, Fig 4-95 (drawing): 24' overall, firebox front to chimney; firebox 4' long, 10' W; ware
  chamber 10' W, a straight section 10' L, then a tapering section 8' L narrowing to 4' W; neck into
  the chimney about 3' W (?); chimney label "4'5" 3'" (?, unclear); "(3) INLET FLUE 13.5 X 9"".
- Side, Fig 4-96 ("inside dimensions"): chimney 14' high; "29" h" at the chimney end (inside height
  there (?)); firebox 4' long and 3.5' deep below the ware floor; two rows of side stoke holes "spaced
  every 27"" (six per row drawn).
- Front, Fig 4-97: arched front with a central door; two stoke holes 13.5" wide × 16" high, one each
  side of the door; an air hole 9" high (same width) under each; width 10'; firebox depth 3.5'.
- Loading: a roller conveyor bridges the firebox "moat" (Figs 4-103, 4-104).
- **Not given:** crown height in the straight section; wall and arch thickness; exit flues; chimney
  section; cone; firing time.

### `meaders-david`: David Meaders's groundhog

- Page: p.115 (text, Figs 4-105 to 4-107). Adapted from his grandfather Cheever Meaders's design.
- Fuel: wood. Draft: cross-draft (groundhog).
- Fig 4-105 (drawing): ware chamber 5' wide, 6' long (the "6'" runs along the side from the
  firebox wall to the back); 30" floor to crown; firebox 4' long (front arch to the low wall); low
  firebox (bag) wall, "18"" printed beside it (the 6' and 18" Checked on the page image,
  2026-10-31); door (dashed) in the front arch.
- Flues: inlet flue box drawn 9 × 4½ (in); exit flue box drawn 7½ (?) × 4½ (in). Counts not stated.
- Chimney: 8' tall, "9" INSIDE" (presumably 9 × 9 in).
- **Not given:** wall and arch thickness; flue counts; grate; ash pit; cone; firing time.

### `hollyweird`: Olsen's Hollyweird Tube

- Pages: pp.116–117 (text, Figs 4-108 to 4-115); p.124 (text); p.194 (photo caption only).
- Built 1985 at Olsen's home pottery. Fuel: wood. Draft: cross-draft (anagama type): a front firebox
  and a second, side-stoked firebox between the chambers.
- Cone and time: held at cone 11-plus for 35–40 h in the front chamber and 10–15 h in the back chamber
  each firing; a "normal" firing is 60 hours (p.117). Fired about twice a year for 25 years: over
  1500 hours at top temperature, over 40 cycles (p.117).
- Construction (p.116): a Bizen-style front chamber joined to a tube-style second chamber. Hard
  firebrick for the walls (?), flues and firebox; IFB for the transition to Thermal Ceramics K-26 IFB
  castable, cast as the two large dome-shaped chamber ceilings. After 25 years (p.117): the K-26 LI
  castable held up better than expected (expansion cracks, but intact); the hard brick slagged,
  spalled and melted at the flues.
- Plan, Fig 4-110 (drawing), front to back: "36" FIRE BOX, DUG OUT ASH PIT …" (?); first chamber ware
  platform 55"; 12" step; wall between the chambers 13"; second firebox grate 15" (a side door here);
  18" step; second chamber ware platform 55"; 9" grate; 6" step; back ware platform 66"; chimney
  inside "15 X 24". Shelves drawn 12 × 24 (in), one 12 × 18 (?). About 249 in (20¾ ft) to the
  chimney (derived). The caption list and the figure labels swap the numbers 4-109 and 4-110.
- Fig 4-108 (sketch): "12'" and "8'" along the two chambers; "55" (Checked on the page image,
  2026-10-31; no unit mark) and "10" (?, faint) at the far end, meaning unclear.
- Front firebox (p.117): the ash pit is the walkway into the chamber, so the grate bars come out
  after every firing; bars ¾ in (2 cm) apart, spaced with broken shelf and wedged with wadding. One
  inlet flue 15 × 18 in (38 × 46 cm); one stoke hole 9 × 13½ in (23 × 34.5 cm) in the door bricking;
  air holes at grate level. In a 60 h firing the ash pit never needs raking.
- Between the chambers (p.116): three large exit flues from the front chamber cross the second
  firebox's grate area, so air passes under and over its grate; pots are also set in these flues.
  Secondary air: a 5 in (12.5 cm) extruded clay tube with graduated holes under the grate, along the
  side, with a shutter or plug outside, through the ash-pit side wall.
- Identity: possibly the same kiln as `olsen-two-chamber` (pp.202–206) and `olsen-anagama-p26`; the
  book doesn't say.
- **Not given:** chamber widths and heights; dome thickness; slope; firebox depth; chimney height;
  damper.

### `gulgong-racer`: Olsen's Gulgong racer, Gulgong, Australia

- Pages: p.76 (text); pp.118–119 (text, Figs 4-116, 4-117); p.120 (captions, Figs 4-118 to 4-124);
  p.121 (captions, Figs 4-125 to 4-128).
- Planned at the 1995 NCECA conference with Janet Mansfield for her Claysculpt Gulgong event (the
  event's year isn't printed); a small kiln for his whisky cups, after Arakawa's teabowl kiln near
  Tajimi; built as "kiln as sculpture" (p.118).
- Fuel: wood. Draft: cross-draft, after the groundhog. Cone 10 (p.119).
- Chamber (p.119): primary ware platform 5 × 5 ft (152 × 152 cm), 3 ft high (lost in the faded
  margin in the scan; read by the user, 2026-10-29); side walls on the upper platform only 1 ft (30 cm) high, sloping down to the firebox
  platform and the door arch. Caption 4-126: interior stacking chamber 5 × 5 × 3½ ft (152 × 152 ×
  107 cm) tall. Capacity "106cu. ft (3cu. m)" (p.119); 5 × 5 × 3½ ft is 87.5 ft³ (derived).
- Firebox (p.119): 5 ft wide, 3 ft deep and 4 ft tall (152 × 91 (?) × 122 (?) cm).
- Steps: 45 cm (18 in) between the two platforms (p.119); a 15 in (38 cm) step from the firebox and
  ash pit up to the stacking platform (caption 4-123). Two steps, or the two pages disagree.
- Roof: dome cast over a dirt-and-wet-sand form under plastic, in Moral Coolcast 140 (Thermal
  Ceramics Australia; "Coolcaste 140" in a caption); outer adobe of dirt, straw and cement; walls
  buttressed with concrete and rocks (pp.119–120). Transitions shaped in insulating castable (p.76).
- Fig 4-117 (drawing): chimney of brick, 5 ft × 9 in, 8 ft tall (the user's reading, 2026-10-29: a
  groundhog's full-width chimney); "4'" and "3'"
  chamber heights (front and middle); "5X5'" ware platform; "5 X 5" firebox; a step "1.5'" (?); grate
  area; ash pit; brick front walls; loading door and stoking; air supply holes.
- Firing (p.119): fire lit outside the door at 4.45 pm and kept overnight; into the firebox at 7 am;
  at 2 pm cone 6 down (the user's reading); under 3 h later cone 10 "into a puddle" and the whole kiln at
  temperature; held with the front air restricted; shut down at 12.30 am. About 10 h from the
  firebox to cone 10 everywhere, about 32 h from lighting (derived).
- Built in four days by a crew (p.119).
- **Not given:** dome thickness; wall thickness; grate size; exit flues; chimney section and height
  (both (?) only).

### `hohr-2003`: anagama-style and fast-fire kilns, Höhr-Grenzhausen, 2003

- Pages: p.122 (text, Figs 4-129 to 4-131); p.123 (captions, Figs 4-132 to 4-139).
- Course at the Art Institute for Ceramics and Glass, Höhr-Grenzhausen ("Westervald" [sic]), 2003: an
  anagama-style kiln and a fast-fire wood downdraft behind it, on a common chimney. Wood; cone 10.
- Like the Gulgong racer but with 18 in (46 cm) stacking platforms each side of the firebox grate and
  entry. Groundhog-style chimney: the left and right flues serve the anagama chamber, the centre flue
  the fast-fire kiln (p.122).
- Fig 4-129 (plan): firebox 1/3, stacking 2/3; "6 (?) 40 X 50CM SHELVES"; chimney built on the
  collection-area foundation. No dimensions in feet or inches.
- Dome cast in "a 2600 IFB (low iron) castable" over a dirt mound skinned with wet sand and plastic;
  dowels for blow holes; a coffee can for a side-stoke hole; buttressed with concrete, rocks and
  rubble; metal grate bars on the firebox ledge (captions p.123).
- **Not given:** chamber sizes, chimney, flues, the fast-fire kiln's size. Can't be modelled.

### `conrad-teardrop`: Conrad Calimpong's teardrop kiln

- Pages: p.116 (caption, "Calimpong"); p.124 (text "Colimpong", Fig 4-140); pp.124–125 (photos,
  Figs 4-141 to 4-147).
- Fuel: wood. Draft: cross-draft; single chamber, teardrop plan, side-loaded; front firebox with a
  grate; chimney at the back.
- Fig 4-140, "ALL DIMENSIONS ARE INTERIOR MEASUREMENTS". Plan: front (firebox) width 39"; grate 15"
  wide at the front centre; widest 51½" (? faint); 48" wide at a station 33" further back; then 16"
  wide (Checked on the page image, 2026-10-31), 12" further on 12" wide, then 19" to the end (last width unreadable).
- Elevation: inside length 9'9"; front height 35½" (?); stoke hole 9" high, its sill 14" above the
  floor; ash pit 12" deep below the floor, 24" long; side door 37" high × 33" wide, its far jamb 48"
  from the chimney wall; height 35" at 24" in front of the chimney wall; exit opening 12" high under
  a 13" block; 8" + 11" = 19" to the back at the base (the 11" faint, but the printed 19" below agrees:
  Checked on the page image, 2026-10-31).
- Chimney: "only 9 x 9in./23 x 23cm square", which Olsen notes fires well (p.124); passive damper
  2½ × 4 (in); marks from the floor 16", 24", 33", 15" (?) up to a damper slot (faint).
- Walls and roof: double side walls (caption 4-144); buttressed with stones and concrete (4-145); a
  cast dome first cast too thin and thickened with more castable (4-146).
- **Not given:** dome and wall thickness; total chimney height; cone; firing time.

### `kannofen`: Kannofen, Art Institute of Ceramics and Glass, Höhr-Grenzhausen

- Pages: p.161 (history); p.162 (text, Fig 6-36); p.163 (Figs 6-37 to 6-41, text); p.164 (text,
  Figs 6-42 to 6-46).
- Fired by Arthur Müller, inside a shed. Fuel: wood, long planks. Salt glaze, with salt ports into
  the top exit flue. Draft: "updraught tunnel kiln": flames run along the tunnel to exit flues in the
  top and sides.
- Length and floor: the floor rises 15 in (38 cm) over the 15 ft (4.5 m) from the firebox end to the
  door end (text).
- Fig 6-37 ("not to scale, all measurements metric"): four arch sections 1.5 m apart, width × height
  to crown: 1.05 × 1.82 m (firebox end); 1.04 × 1.69; 1.07 × 1.56; 1.05 × 1.43 (far end, "BACK
  ENTRANCE"). Floor steps +15 cm, +26 cm, +38 cm "RISE"; 3 × 1.5 m = "14'9"". The crown stays level
  (derived: 1.82 − 1.43 = 0.39 m against a 0.38 m rise).
- Fireboxes: two, with "GRATE BARS ON BOTH SIDES" and a brick wall between two ash pits; grate bars
  in the middle and either side of the flue channels; "4 FLUE CHANNELS 15CM WIDE"; 25 cm, 40 cm,
  25 cm between channels and fireboxes (meaning unclear). "1840cm" along the length and "1400cm"
  across the firebox front fit neither size (**Flagged**).
- Setting: about 600 greenware setter tiles 1¼ × 1¼ in (3 × 3 cm) × 10 in (25 cm) over the flue
  channels: tight for the first 4 ft (122 cm), then "about  in. (1cm)" apart (fraction missing,
  **Flagged**) for 6 ft (183 cm), then ¾ in (2 cm) grading to 1¼ in (3 cm), the last 8 in (20 cm)
  open; shelves on rowlock brick.
- Exit flues: seven rows; the two nearest the firebox closed, row three dampered, the last four open
  (p.164).
- The text calls the firebox end the "back" and the far end the "front or door end"; the drawing
  labels the far end "BACK ENTRANCE" (**Flagged**).
- **Not given:** wall and roof thickness; firebox sizes; exit-flue sizes; cone; firing time.

### `olsen-anagama-p26`: Olsen's anagama-style kiln

- Page: p.26 (text).
- Hot face of Thermal Ceramics K-26 IFB, in service over 25 years; it resisted wood-ash slag
  "superbly", better than hard brick of the same rating.
- It may be `hollyweird` (also about 25 years old, also K-26), but there the hard brick slagged and
  the domes are K-26 castable; the book doesn't link the two.
- **Not given:** any dimension.

### `bayer-tube-form`: Svend Bayer's tube kiln

- Page: p.50 (Fig 2-27A, photo by Svend Bayer): laying bricks over a slatted tube form for a
  groundhog, anagama or tube kiln.
- **Not given:** any number.

---

## 7. Round, bottle and folk kilns

### `pit-kiln-improved`: improved pit kiln (type)

- Page: p.152 (text, Fig 6-2).
- Fuel: sticks, grass and dung. Draft: primitive updraft.
- Fig 6-2 (drawing): wall height 3'4"; base "4'12"" (as printed: the user's copy says the same, and
  the user takes it for 4'10"; **Flagged**).
- Fuel is stuffed between the pots and the wall; stoke and air holes round the perimeter; a dome of
  clay and straw, or shards, dirt and straw, mudded over; fired until the dome is red-hot.
- Used in folk potteries in Spain, Nigeria and Mexico, and villages in Africa, India and South
  America.
- **Not given:** wall thickness; stoke-hole sizes; firing time.

### `baobab`: Baobab-type kiln, Niger (type)

- Page: p.153 (text, Fig 6-3). The floor stands on an umbrella of flexible branches, small trunks and
  fagot bundles, reinforced with clay and plastered. Egypt: perforated clay-brick shelves from a
  middle post in the firebox (also Crete and Greece). Drawing labels: shard dome, chamber, flues,
  firebox.
- **Not given:** any number.

### `moveros-umbrella`: umbrella kiln, Moveros, Spain

- Pages: p.153 (text, Fig 6-3); p.154 (text, Figs 6-4 to 6-7).
- Fuel: heather and any brushwood. Draft: updraft. Still fired in the mid-1970s.
- Chamber: about 5 ft (150 cm) in diameter (text). Fig 6-3 (drawing): 5' across the top; chamber 4'
  tall ("pots never past top of kiln"); firebox 3½–4'; a "step"; firebox mouth 27" high × 22"
  wide (Checked on the page image, 2026-10-31).
- Walls: granite rocks mortared together, 18 to 24 in (46 to 61 cm); firebox and chamber plastered
  with clay inside.
- Floor: an umbrella floor of spokes on a central trunk over the firebox; shards fill the gaps.
- Roof: none built; pots piled to the top, shards stacked over them.
- Firing (p.154): started at the firebox mouth; after two hours the brush is pushed further in and
  stoked faster for about six hours; done when flames come out of the top; coals put on top during
  firing; ashes and coals poured in at the end.
- **Not given:** floor details; firebox plan; temperature.

### `greek-updraft`: early Greek updraft (type)

- Page: p.154 (Fig 6-8): "slightly domed over but with center support"; exit flue in the dome;
  chamber with door; firebox beside, its inlet flue up through the floor.
- **Not given:** any number.

### `singh-lowfire`: Mansimran Singh's low-fire glaze kiln (early Muslim design), New Delhi

- Pages: pp.155–156 (text, Figs 6-9 to 6-13). Built by Singh's father; "a Muslim design dating from
  antiquity".
- Fuel: wood, hardwood logs 2 to 6 in (5 to 15 cm) in diameter. Draft: updraft. Ware: Delhi Blue
  tiles and low-fire glazed pottery, all but the tiles saggared.
- Firing (p.155): about five hours to warm the firebox, then about six to seven hours; coals shoved
  into a pit under the chamber, so the chamber reaches 500 °F (260 °C) gradually.
- Section, Fig 6-12 (drawing): setting height 5'; domed floor carried on the inlet flues; firebox 4'
  long; 2' at the firebox entry, from the ground line down to the pit floor; 2'6" from the domed
  floor's underside down to the pit floor (both Checked on the page image, 2026-10-31); "pit line (for coals and embers)".
- Plan, Fig 6-12 (drawing): chamber 5' inside diameter; six rectangular inlet flues, one marked
  4" × 4", the top pair 10" apart, plus a central round flue; a side entrance from the firebox 12–15" (read by the user, 2026-10-31); a
  note on the round flue diameters cut off at the page edge.
- Roof: shards and saggar pieces piled in layers over the setting.
- **Not given:** wall thickness; round-flue sizes; firebox width; temperature reached.

### `ninodaguia`: Niñodaguia kiln, northwest Spain

- Pages: pp.156–157 (text, Figs 6-14 to 6-18). A commercial pottery.
- Fuel: wood ("fired with pine…", next word cut). Draft: updraft.
- Fig 6-14 (drawing): chamber 7' diameter, 3½' tall; chamber walls 15½"; "9 rows of bricks up"; firebox
  3'; 18" (a wall or step beside the firebox); a ledge "up for dome first bricks"; firebox mouth 27"
  high × 18" wide.
- Floor: a dome of common bricks in circular soldier courses with a very shallow rise to a 12 in
  (30.5 cm) keystone; 1½ in (3.8 cm) holes through the floor bricks are the inlet flues. Dome brick
  9" × 4½" × 2½" with grooves and two holes (drawing).
- Firebox and chamber about equal in height and width (text).
- Capacity: 2000 to 3000 small pots or about 1000 large ones. Set 8 or 9 high on setter tiles, shards
  over the top as the roof.
- **Not given:** firebox plan; flue count; firing time; temperature.

### `miravet`: Miravet medieval kiln (old and new), Catalonia, Spain

- Pages: p.157 (heading); p.158 (text, Fig 6-19); p.159 (text, Figs 6-21 to 6-26); p.160 (text, Fig
  6-27).
- Fuel: wood: long wood, then wood chips, bundles, grass, slash and thin slats. Draft: updraft.
- Layout (p.158): three equal cubes: a domed chamber, a sub-chamber below it (a cube less the floor
  arch, holding the inlet flues and also stacked with pots) and, in front, a firebox cube that is
  firing chamber and ash pit in one. No grates.
- Fig 6-19 (drawing): chamber 8' × 8' I.D.; 6' high to where the dome starts (the arrow ends at the dome's lower edge: Checked on the page
  image, 2026-10-31); 9' to the dome crown;
  dome main flue 15" diameter; four corner flues 5"; walls 3–4' thick, partly buried; floor 13–15"
  thick at the centre; floor flues all 6" × 6", 35 in all; lower cube 8' × 8' I.D., heights 8' and
  6'6"; firebox mouth 27" high × 18" wide; 3' (from the mouth sill down; Checked on the page image, 2026-10-31).
- Flues: the four corner dome flues are exit and control flues; close some to send heat to others,
  pull a plug over a cold area (p.158).
- Firing, new kiln (pp.159–160): stacked "plumb full"; glazed target pots on the sub-chamber bag wall
  and by the centre dome flue; the two dome flues nearest the firebox closed at the start; long wood,
  several armfuls every 4 to 5 minutes until the target pot darkens; then wood chips, six shovelfuls
  at a time rising to 30; done when the target pots in the dome flues are done: **28 to 32 hours**.
- **Not given:** firebox plan size (presumably the third cube, not stated); dome thickness;
  temperature.

### `falcone-pompeii`: Falcone Pompeii updraft, Fornace Falcone, near Montecorvino Rovella, Italy

- Pages: p.160 (text, Figs 6-28 to 6-30); p.161 (text, Figs 6-31A to 6-35).
- Fuel: wood, long slats, no grates; 15 tons (13.6 metric t) a cycle. Draft: updraft, a Pompeii-era
  design like Miravet. Ware: replica tiles and bricks for restoring Pompeii.
- Ware chamber: 118 in (3 m) wide, 157 in (4 m) deep, 79 in (2 m) tall, **848 cu ft (24 m³)**; holds
  80,000 bricks or about 20 tons (18 metric t).
- Firebox chamber underneath: same plan, 71 in (1.8 m) tall, 763 cu ft (21.6 m³). Both volumes check
  (derived).
- Temperature: usually 1760 °F (960 °C), at most 1922 °F (1050 °C). Cycle about 40 hours.
- Floor: firebox ring arches 9 in (23 cm) apart span the chamber and carry the floor; arch bricks
  form the flue holes; a first tile layer at right angles lets the gas circulate.
- Exit flues: three across the back, front and middle of the arch roof, nine in all, evenly spaced
  (Fig 6-32 shows a barrel vault with square holes).
- Firebox: stoking port with an under-air supply (caption 6-34).
- Construction: modern firebrick inside, a façade of old tiles.
- **Not given:** wall thickness; vault rise and thickness; exit-flue size; stoking port size.

### `kenzan-muffle`: Kenzan enamel kiln (kin-gama), a muffle kiln

- Page: p.165 (text, Fig 6-47). From a 1915 sketch in Bernard Leach's notebook, found in Tomimoto's
  studio; the design dates back to the Sung dynasty (950–1250).
- Fuel: wood ("FIREBOX (wood)"). Draft: updraft round a muffle. For overglaze enamels and
  reduction-sensitive colours.
- Fig 6-47 (drawing): top outside diameter "2½" (unit not printed; probably ft); wall 4" thick;
  firebox 2' wide × 2' high; iron grate opening 15" × 19"; muffle 2½' tall, 16–18" diameter, wall ½"
  (Checked on the page image, 2026-10-31), "7 holes in each band" (two bands); lid with lip and an exit flue "DM 6""; wedge supports
  between muffle and wall; muffle on a pedestal marked "12'" (**Flagged**, surely 12 in).
- **Not given:** outer height; temperature; firing time.

### `bottger`: Böttger circular updraft, Germany, about 1700

- Page: p.166 (text, Fig 6-48). Coal and coke. A cylinder with three evenly spaced fireboxes at the
  base (grates, bag walls, stoke holes, air and ash pits); a dome with exit flues into a cone-frustum
  chimney; arched door; ware saggared.
- **Not given:** any number.

### `breda-bottle`: Breda bottle kiln, Segra Pottery, Breda (near Barcelona), Spain

- Pages: p.166 (text); p.167 (text, Figs 6-49 to 6-51); p.168 (text, Figs 6-52, 6-53).
- Builder: the local clay supplier, August 1979, for domestic earthenware with lead glazes.
- Fuel: wood, chestnut slats 3 ft (91 cm) long, "some 2 tons (about 18[00?] kg)" a firing (metric cut
  at the gutter). Draft: updraft into a bottle (cone-frustum) chimney.
- History: at first no ash pit; the small firebox (about 3 ft to the floor dome, sloped sides)
  choked; the cone drew more but ash choked it again; the fix was a grate with an ash pit below,
  with equal volume above and below the grate (pp.166–167).
- Fig 6-50 (drawing): chimney bottle 25' high, 12' across at its base; chamber 15' diameter × 7'
  high; kiln wall 2' thick with metal banding; dome ceiling with chimney holes; domed floor; firebox
  3' from grate to floor dome; ash pit 2' wide × 3½' deep.
- Fig 6-51 (drawing): inlet flues 4½" × 4½"; 27" from the wall to the first flue line, 18" to the
  next; perimeter flues 27" apart; "2"" at two flue lines (meaning unclear); a 2' bag wall with
  openings 9" apart; firebox 3' high, its floor sloping up sharply to the walls; metal grate on a
  1' ledge (Checked on the page image, 2026-10-31); "GRATE BARS 1" APART AND RUN 8' INTO FIREBOX (37 total grate bars)".
- Fig 6-53 (drawing): 8 dome exit flues in the centre; "21 – 4½ × 5" exit flues" round the perimeter
  with damper blocks; chimney-cone holes 7" × 15", one per exit flue, 15" apart; 9" walls in the cone;
  a door in the cone.
- Firing (p.168): pots set off the floor; slow preheat of "about 3 (?) hours" (digit at the gutter);
  stoking builds to every 4 minutes by the end of 7 hours; stoke when the flames at the cone holes
  suck back in; about 10 hours in all; evenness by damping the dome flues. Clean out the ash pit after
  each firing.
- The text says Fig 6-54 shows the envelope kiln that replaced it; Fig 6-54 is the two-storey bottle
  kiln (**Flagged**).
- **Not given:** dome rise and thickness; firebox plan; temperature.

### `bottle-two-storey`: two-storey bottle kiln, mid-1800s (type)

- Pages: p.168 (text, Fig 6-54); p.169 (text). Coal or coke; glaze chamber below, bisque above.
  Labels: "center flue off firebox"; "extremely thick dome (2' or more)". Huge walls, heavy iron
  bracing, uneven firing, long cycles (p.169).
- **Not given:** any size beyond the dome's 2'.

### `sevres`: Sèvres Porcelain Factory two-storey bottle kilns

- Pages: pp.168–169 (text, Figs 6-55 to 6-58). Built about 1880, used for porcelain into the
  mid-1990s; saggars; iron banding in the photos.
- **Not given:** any number.

### `milton`: Milton's two-chamber kiln, England, patented 1873

- Page: p.169 (text). An updraft combined with a downdraft.
- **Not given:** any number.

---

## 8. Multi-directional kilns

### What all four share (Olsen's concept, pp.178–180)

- Two cross-draft systems at right angles share one fire zone: an anagama-style tube crossing a
  modified groundhog. Each firebox faces its own chimney across the zone and is also the chamber's
  door (pp.178–179).
- Chimneys (p.179): the groundhog chimney is split into thirds, each flue with its own passive air
  and shelf damper; the anagama chimney is single, with passive air and a shelf damper. Both are of
  equal height and slightly tapered.
- Fig 7-2 (drawing): "FOREZONE AREA: DIAGONAL – 7' (CHURCH); DIAGONAL – 9' (FIREWORKS)".
- Fig 7-3, firebox (drawing): "STEP UP TO WARE PLATFORM 12–15""; firebox/grate "3–4' NORMAL" long;
  "ASH PIT AND WALKWAY" 14" wide, 18" deep (Checked on the page image, 2026-10-31); chamber width and door size optional; triangular
  posts and "¼" thick shards" for spacing.
- Fig 7-4: air at three adjustable levels: ash pit below the grate, at the grate, and the stoke hole
  above it, built into the bricked-up door.
- Fireboxes (p.180): the anagama firebox is the largest, the slow starting firebox, because its
  single chimney is the smaller; the groundhog firebox has a smaller entrance straight into the
  chamber, for blasting.
- Fire zones about 3½–4½ ft (107–137 cm) to the vertex of the ceiling (p.183).

### `fireworks-edmonton`: Fireworks kiln, Edmonton, Alberta, 1998

- Pages: p.181 (text, Figs 7-5 to 7-7); p.183 (text); Fig 7-2.
- Fireworks, the Edmonton International Ceramics Seminar, "University of Edmonton" (as printed),
  1998. Built in a pre-conference workshop by 40 participants: "in four days" against "the three-day
  workshop" in the same paragraph (**Flagged**). No plans; drawing version 2 (Fig 7-6) was posted on
  site. The first multi-directional prototype.
- Fuel: wood. Cone 10-plus.
- Fire zone: "approximately 9ft (274cm) in both directions" (p.183); "DIAGONAL – 9'" (Fig 7-2); about
  3½ to 4½ ft (107 to 137 cm) to the ceiling's vertex (p.183).
- Chimneys: a single tall chimney and a three-flue groundhog chimney (photo 7-7); the dome covered in
  stones or shards.
- **Not given:** firebox sizes; chimney sizes and heights; walls; dome thickness; firing time.

### `church-skaelskor`: Church kiln, Skælskør (Guldagergaard), Denmark, 1998

- Pages: p.180 (text); p.182 (text, Figs 7-8 to 7-10); p.183 (text); Fig 7-2.
- Built by Olsen at a workshop for Nina Hole at the new International Ceramic Center, 1998; styled on
  the white church at Ørslev; roof like an upturned Viking longboat, whitewashed. Built beside an
  Olsen 36 gas kiln. Fuel: wood. The second multi-directional kiln.
- Fireboxes: the smaller, 24 in (61 cm) wide, faces the groundhog chimney; the larger, 36 in (91 cm)
  wide, faces the single anagama chimney (p.182).
- Fig 7-9 (drawing): "9 BRICKS TALL 28–30"" (back wall or groundhog chimney top); single chimney
  13.5 × 13.5"; walls 9" thick; "18" STEP DOWN"; walk-in channels below ground; two "FIREBOX GRATE,
  ASHPIT AREA"s.
- Fire zone: 7 ft (213 cm) (p.183); "DIAGONAL – 7'" (Fig 7-2); about 3½–4½ ft to the ceiling's vertex.
- **Not given:** chimney heights; groundhog chimney size; firebox lengths; roof construction; cone;
  firing time.

### `kecskemet-multi`: Kecskemét kiln, International Ceramic Studio, Hungary

- Pages: p.182 (text); p.183 (text, Fig 7-11). Printed "Kesckemét".
- "The second and largest cross-directional kiln in Europe." Wood. Fireboxes dug down; a channel
  between them takes a bench; styled after the courtyard columns, yurts and Hungarian roof tiles. Fire
  zone "larger" than the Fireworks kiln's 9 ft (p.183). Photo: brick ring-arch door, tiled roof.
- **Not given:** any dimension.

### `kanayama-multi`: Kanayama kiln (multi-directional)

- Pages: p.183 (text); p.184 (Figs 7-12 to 7-16); p.185 (Figs 7-17 to 7-20A, text); p.186 (Figs 7-21 to
  7-26, text); p.187 (Figs 7-26A to 7-29, text); p.188 (Figs 7-30 to 7-33, text); p.189 (text).
- Builders: Olsen with Ryoji Matsuyama and Lee Middleman, on a shallow hillside (place not named on
  these pages). The note on pp.137–138 spells the owner of the Kanayama oil kiln "Ryoji Matsumiya";
  the spelling isn't resolved.
- Fuel: wood. Cone 9/10 by the evening of the first full day. Draft: a groundhog firebox with a
  three-flue chimney and an anagama firebox with a single chimney.
- Fire zone: sized to 16 kiln shelves, plus three in each firebox area (Fig 7-12). The shelf size
  isn't printed.
- Fireboxes: dug at right angles, "just over 2ft (61cm) deep"; seven brick courses up to floor level
  (pp.183–185). Grate bars ¾ in (2 cm) apart; air holes in the door at grate level; ash-pit entrance
  fully open; stoke hole 9 × 13 in (23 × 33 cm) in both doors; 9 to 12 in (23 to 30.5 cm) rise from
  the grate to the chamber floor (pp.188–189).
- Walls (p.186): 9 in (23 cm), as are the chimneys, straight up "1?" rows (digit cut at the page edge),
  then a header course slanted inward, the row-14 bricks angled further, as the transition to the
  castable. Ring-arch doors on arch frames, one per firebox. Outside walls buttressed with dirt,
  rocks and concrete.
- Dome (pp.186–188): cast over a collapsible frame decked with plywood, shaped dirt, wetted sand and
  plastic; castable built up from the perimeter **5 to 6 in (12.5 to 15 cm) thick**; cured 24 hours
  under wet towels and plastic; the dirt then dug out and heaped over the kiln.
- Chimneys: the groundhog collection box divided into three chimney flues, each with a damper and
  passive-air bricks (Fig 7-19).
- Firing (p.189): lit about 10 pm outside the single-chimney firebox; onto the grate next morning;
  cone 9/10 by evening, held overnight; then the other firebox fired hard, then hours of alternating.
- **Not given:** fire-zone size; chimney heights and sections; firebox lengths; castable product.
  Can't be modelled.

---

## 9. Electric kilns

### `electric-car-45`: the widest electric car kiln Olsen knows

- Pages: p.244 (text); p.245 (text, top cut by the page curve).
- Inside: width 45 in (114 cm), length 106 in (2.69 m), height 49 in (124 cm). Elements in the sides
  (the next word is cut: "and floor" (?)). About 135 ft³ (derived).
- **Not given:** maker, power, voltage, cone, walls.

### `jiesia`: Jiesia bone-china factory car kilns, Kaunas, Lithuania

- Page: p.245 (text, Figs 9-1, 9-2, 9-2A). Large electric car kilns; roll-away cars on neoprene
  wheels; German shelf-and-post system; side-wall elements.
- **Not given:** any number.

### `job-forni-hobbyker`: Job Forni "Hobbyker" front-loading kilns, Cartigliano, Italy

- Page: p.248 (text, Fig 9-15). A single grooved wall unit of Thermal Ceramics M-Board; element grooves
  at the recommended 2½ in (6.3 cm) spacing; the hairpin turn hidden in the butt corner joint; a
  louvred heat shield and dead-man air space built into the 6 in (15 cm) wall. Olsen Kilns are the US
  contact.
- **Not given:** chamber size, power.

### `electric-reduction-smoke`: electric kiln with a wood smoke firebox

- Page: p.250 (text, Fig 9-25, plan and section).
- An outside wood firebox feeds smoke, not heat, through inlet flues in the floor; it leaves by an
  exit flue high in the end wall and a chimney, both opened when reduction starts. Stoke kindling, let
  the smoke clear a little, repeat. Reduction shortens element life: alternate with oxidation.
- Fig 9-25 (drawing): two flue channels under the floor, 4½ in wide, four flue holes each, "Largest flue
  holes further from firebox": 1½ in, 1¼ in and ¾ in diameter (three sizes for four holes); a 5 in
  channel flue below the floor at ground line; exit flue 4 × 6 in; chimney 6 × 6 in with a damper; vent
  holes in the roof. Firebox below and outside: grate; ash pit 18 in wide; stoke hole; a sloped stoke
  box "18" deep"; 4½" between the stoke hole and the air inlet; air inlet 9 × 12 in.
- **Not given:** chamber size, power, cone.

---

## 10. Oil and coal kilns

### `kato-coal`: Mr Kato's coal downdraft, Kato pottery, Tajimi, Japan

- Pages: p.131 (text, Fig 5-4); p.132 (text, Figs 5-5 to 5-8); p.207 (text, Fig 8-18). Called a
  "Downdraft Tajimi-style kiln".
- Fuel: coal, later converted to oil burners to save labour. Draft: downdraft: two side fireboxes with
  grates and bag walls, floor exit flues into channels, a collection box, a round chimney.
- Size: "approximately 250cu. ft (7cu. m)" (p.131).
- Firing (p.131): "The kiln is fired in over 50 hours to 2372F" (the 50, lost in the margin in the
  scan, read by the user, 2026-10-29), in very heavy reduction;
  cooled three days or more; slow because of the very thick walls and only two fireboxes. Above
  2000 °F (1090 °C): reduction 10 to 12 shovels of coal every 20 minutes, oxidation 3 to 4.
- Section, Fig 5-4 (drawing): chamber 6'6" wide wall to wall and 6'6" floor to crown; "1'" from the
  top of the setting to the crown; bag walls 36" high, 4'8" apart (inside faces); exit flues drop
  through the floor into flue channels 18" deep; grate bars at a slope, ash pit below, firebox floor
  below ground; vapour holes in the arch. The arch is drawn thick; no thickness printed.
- Plan, Fig 5-4 (drawing): the user reads that the length isn't printed and has to be added up
  from the plan's parts (2026-10-29); the earlier reading was length "7'" (? could be 9'; 7 × 6.5 ×
  about 5.5 ft ≈ 250 ft³ fits the
  text, derived); width 6'6"; walls 10" at the door end; door in one end wall; bag walls about 6"
  thick along the long sides, "6"" and "9"" from the wall at the end; "12 FLUE HOLES 6" X 6"" in three
  rows over three flue channels; one firebox mouth with a "REMOVABLE GRATE, 1" IRON ROD BUILT INTO
  WALL", the other "ARCHED"; each opening into the chamber 4' long, 2'6" wide at the outer mouth;
  "30"" at the outer wall; a 20" wide connection to the chimney with a damper (10" wall). The 10"
  (door end and chimney wall) and the 30" were checked on the page image, 2026-10-31; the length's
  digit reads 7' (read by the user, 2026-10-31).
- Chimney: round, 3' inside diameter at the base, with an atmosphere damper; "CHIMNEY 20' TALL
  TAPERING TO 15½"" (Checked on the page image, 2026-10-31).
- Flue areas (pp.131–132): floor exit flues 432 in² (0.28 m²), 12 × 6 × 6 in; inlet flues from the
  fireboxes about 500 in² (0.32 m²), "a bit larger"; damping the air when firing evens them.
- Proposed redesign (Fig 5-5): 6 × 6 in flue holes in a 9" floor over channels 9–18" deep and 9" wide
  into a collection box; chimney flue 24" × 18" = 432 in²; chimney 18" × 18" = 324 in² at the top.
- Walls and bag walls (p.132): bowed walls curl the flame down to the centre sooner (Fig 5-6); bag
  walls "just a few feet shorter than the chamber length", with a large enough firebox opening.
- Grates (p.207, Fig 8-18): 5 ft² (0.46 m²) per firebox (text); drawn 30" × 22" = 660 sq in,
  labelled "5 sq ft" (660 in² is 4.6 ft², derived). Floor 30 ft² (p.207). The figure prints "10 sq ft
  per 30 sq ft floor; 6 to 1 ratio; 30 / 6 = 5 sq ft of grate per firebox" (**Flagged**: floor ÷ ratio
  is the total grate, and two such grates make about 3.3:1).
- The floor areas don't agree: 30 ft² (p.207) against 6'6" × 7' (?) = 45.5 ft², or 4'8" between the bag
  walls × 7' = 32.7 ft² (derived).
- **Not given:** firing hours (lost); arch thickness; side-wall thickness; firebox heights.

### `singh-coal`: Mansimran Singh's round downdraft, Delhi Blue Pottery, New Delhi

- Pages: p.133 (text, Fig 5-9, Table 5-1); p.134 (text, Figs 5-10, 5-11); p.135 (text, Figs 5-12 to
  5-16); p.207 (text, Fig 8-18).
- Fuel: coal ("Steam coal, Grade B, is usually used"), started with wood and kerosene. Draft: natural
  downdraft, round, domed, four fireboxes.
- Cone: "Cone 10 oxidation to middle-fire" (p.133, first word faded); up to 2½ cones between top and
  bottom, by weather and coal.
- Size: "approximately 385 cu. ft (11cu. m)" (p.133; the 385, faded in the scan, read by the user,
  2026-10-29). The drawing's 7 ft diameter, 5 ft to the springline and 2 ft dome give about 235 ft³
  (derived), so the printed volume and the drawing disagree (**Flagged**).
- Firing (Table 5-1), per firebox: hours 1–3, 1 shovel every ½ hr, fire mouth open; 4–6, 2 shovels
  every ½ hr, fire mouth bricked up; 7–12, 3 shovels every 45 min; 12 to end, 4 shovels every 50 min,
  glaze tiles drawn; 19, 5 shovels every 50 min. Total 19 to 20 hours; poorer coal up to 30.
- Plan, Fig 5-10 (drawing): chamber 7' diameter; four arched fireboxes with "EXTRA BRICK BRACING
  BETWEEN FIRE BOXES"; arched door; "OUTSIDE COAL PIT AREA (4' X 2')" at each firebox; "FLOOR EXIT FLUE
  HOLES 6" X 6" EVENLY SPACED", 12 drawn, 12" apart along the rows, 10" and 18" across (432 in²,
  derived); "FLUE CHANNEL 24" X 16"" to the chimney; chimney inside "24" X 24"". The chimney is 30' tall,
  about 25–30' from the chamber (read by the user, 2026-10-31; the scan washed out at 500 dpi).
- Section, Fig 5-11 (drawing): wall 5' floor to springline; dome rise 2' (about 7' to the crown,
  derived); cooling and vapour holes in the dome; floor 9" thick over a flue collection channel 12"
  deep; floor flue openings drawn 9" wide (the plan says 6" × 6"); firebox 24" wide inside with a 9"
  outer wall, 40" overall; heights 15" + 15" + 36" (which is which unclear); arched over; round grate
  bars (four drawn); "STOKING HOLE 15" X 13"" (read by the user, 2026-10-31); "AIR SOURCE AND COAL ASH PIT 36" X 24""
  (?).
- Bag wall (p.134): no freestanding bag wall; the chamber wall is notched 9 in (23 cm) deep by 2 ft
  (61 cm) wide and 3 ft (91 cm) long at each firebox, with a firebox flue entrance of 15 × 24 in
  (38 × 61 cm) (the drawing says 16" high, sill 24" above the floor). Fig 5-16: recess 2' wide, 2'
  tall (?), its top 9" to 15" above, 2' from the floor (?); the notch tapers into the dome (Fig 5-15).
- Setting (p.135): saggars, stacked to within 6 to 8 in (15 × 20 cm [sic]) of the dome, about 12 in
  (30.5 cm) clear round them up to the skewbacks.
- Grates (p.207, Fig 8-18): 4 ft² (0.37 m²) per firebox (text); drawn 24" × 24" = 576 sq in = "4 sq
  ft". Floor 38 ft², metric printed "5.53" m² (**Flagged**: 3.53). The figure prints "16 sq ft per 38 sq
  ft floor; 8 to 1 ratio; 38 / 8 = 4+ sq ft of grate per firebox" (**Flagged** as for Kato).
- **Not given:** dome and wall thickness; chimney height; damper.

### `kanayama-oil`: Kanayama oil downdraft (Olsen, July 2005)

- Pages: p.137 (text, Figs 5-22 to 5-26); p.138 (text, Figs 5-27 to 5-34).
- Built by Olsen at the Goshogawara International Woodfire Festival, Japan, for Ryoji Matsumiya.
- Fuel: oil, "fired from the back with two oil b[urners] on each side of the chimney" (two in all or
  two each side: unclear); oil and air lines to each burner (an air-atomizing burner). Draft: "a basic
  downdraft". Use: *hidasuki* in oxidation at a middle stoneware temperature.
- Layout (caption 5-22): kiln shelves laid on the ground to set the plan; "the firebox width of 7in.
  (18cm) and the 7in. (18cm) wall and a 7in. (18cm) back wall"; front flue collection area and door
  seal laid out.
- Materials: IFB, with hard fireclay brick in the firebox areas, the subfloor and the lower bag wall
  (captions 5-24, 5-27); door laid in 2600 IFB (5-25).
- Frame: welded angle iron, matched to the brick sizes, "to make it portable" (5-23, p.138).
- Arch: skewbacks with back-up bricks; a sealer arch against the door; the main arch laid on a form
  between the sealer arch and the back wall (5-29 to 5-31). Bag wall and shelf supports in the centre
  (5-32).
- Chimney: "9 x 9in. (23 x 23cm)" (caption 5-28).
- p.138 cites "Fig. 5-21" for how the dimensions were found; that is the Kähler kiln (**Flagged**).
- **Not given:** chamber size; shelf size; burner type and rating; arch rise; chimney height. Can't be
  modelled.

### `olsen-oil-drip`: Olsen's gravity-drip oil kiln

- Pages: pp.207–209 (text, Figs 8-19, 8-20).
- Fuel: #2 diesel by choice; kerosene and #1 also burn clean; he once fired "my kiln" on free used
  crankcase oil (p.209). Cone: Seger cone 10 (p.208).
- Size: a 45–60 ft³ (1.27–1.7 m³) kiln with three channel ports (p.208).
- Fuel per firing: about 60–75 US gal (227–284 l) of #2 diesel to cone 10 (p.208).
- Drip units: three inlet port flues, three plates per channel, nine plates (p.207). Plates 9 × 5 in
  (23 × 12.5 cm), parallel, each 3 in (7.5 cm) below the one above, overlapping it 2 in (5 cm), sloped
  about 2 in 9 (2:9 to 2.5:9 for diesel); iron with welded pegs and a side lip. Stack about 16" tall,
  channel 6" wide (Checked on the page image, 2026-10-31), port flue 9" (drawing). Set in loosely laid brick so they can be
  adjusted. Side-firing units: 12" × 15" iron plates on an iron frame, tilted (drawing).
- Drip ports: at most one per 9 in (23 cm) of inlet-flue wall, at least one per 18 in (46 cm);
  starting 4½ in (11.5 cm) from the corner fits one or two more (p.208).
- Feed: gravity from a tank 10 ft (3 m) above the plates; three gate valves; funnels and brass tubing
  to each channel's top plate (p.208). Fig 8-19: a 20 gal drum, gate valve, ¼" brass joints and tube.
- Firebox inside the chamber: like a side-stoking channel in a climbing kiln, at least 9 in (23 cm)
  from the wall to the bag wall, the length of the chamber and up the wall (p.208).
- Fig 8-20's caption says "coal kiln"; it shows the oil plates (**Flagged**).
- **Not given:** which kiln this is; chamber dimensions; draft; flues; chimney.

### `leach-chamber`: Bernard Leach's chamber kiln

- Pages: p.210 (text); p.213 (Fig 8-34 drawing, Fig 8-35 photo).
- Fuel: oil, Denver-type low-pressure forced-air burners. Several chambers ("secondary air for use in
  firing 2nd and 3rd chamber").
- Fireboxes outside the chamber (drawing): two, each 17" wide and 3' deep, 40½" overall; an inlet
  flue from each; a wide spray angle, "45° +". Front: burner blocks; "6"" and "6""; 17"; a shallow
  arch; height cut off ("?2"").
- **Not given:** chamber sizes and count; flues; chimney.

### `park-tuscarora`: Denis Park's Tuscarora drain-oil kiln

- Pages: pp.209–210 (text, Figs 8-23, 8-24); p.224 (text).
- Fuel: diesel to start, then crankcase oil; a kerosene line; water by needle valve from red heat,
  up to about 20 % of the mix (p.210).
- Firebox: 9 in (23 cm) wide, with a built-in curved deflector that turns the flame up and cuts
  slagging (p.210). Labels: combustion channel, oil burner, exit channel, chimney, deflector.
- Burner (drawing): nozzle a 2" pipe, 16" long; blower a Clements Cadillac HP3; air gate valve; 55 gal
  drum insulated with 1" Armaflex; sediment bowl; a 1000 W engine-block heater; three needle valves
  (oil, kerosene, water) into one funnel; oil pipe ⅜" I.D.
- **Not given:** chamber size, draft, chimney.

### `soldner-raku`: Paul Soldner's raku kiln and kerosene burner

- Page: p.210 (text, Fig 8-26). Kerosene, gravity-fed; a full-force burner used once "the little
  kiln" is hot.
- Burner (drawing): 2" pipe 12–15" long; a 2" to 1" reducer at one end, a vacuum-cleaner nozzle at the
  other; a ¼" pipe soldered in at an angle 1½" from the reducer end; gate valve.
- **Not given:** the kiln's size or shape.

---

## 11. Worked examples

These are not whole kilns, or are kilns drawn only to show a rule. They make good test cases.

### Flues, chimneys and grates (Chapter 3)

- **W1. Fast-fire chimney from the grate, 10:1** (p.77, Fig 3-8, "Wood guideline, draft kiln (ratio
  10:1)"). Version A: two fireboxes 9 in × 45 in = 405 in² each (drawing), "810sq. in." of grate
  (text); ÷ 10 → chimney 81 in² = 9 × 9 in; inlet flue drawn "4½ x 9"" (faint). Version B: "If the
  draft grate area is 1215sq. in. (7839sq. cm)": two fireboxes 13½ in × 45 in = 607.5 in² each
  (drawing); inlet flues 4½ × 13½ in; ÷ 10 → chimney "121½ sq. in. or 9 x 13½in. (784sq. cm)".
- **W2. Cross-draft wood kiln** (p.77, Fig 3-9). Firebox 60 in "sidelong" × 36 in deep = 2160 in²
  (13,935 cm²) of grate; ÷ 10 = 216 in² → 12 × 18 in (30.5 × 45.7 cm), built as 13½ × 18 in to fit
  brick, "(243 sq" brick size)" (drawing). With a side stoke of 9 × 60 in = 540 in²: "2160 + 540 ÷ 10
  = 270 Sq"" → 13½ × 22½ in "(304 sq" brick size)". Round results **up** to brick sizes. **Flagged**
  metric: "60in. (387sq. cm)" (60 in is 152 cm); "13½ x 18in. (87 x 116cm)" (about 34 × 46 cm).
- **W3. Groundhog, 4:1** (p.77, Fig 3-10). Firebox 36 in × 60 in = 2160 in², marked "1/3"; the rest of
  the plan "2/3"; a 9 × 60 in strip of 540 in² (side stoke). "Approximately, a 4-to-1 ratio". No
  chimney size drawn.
- **W4. Updraft gas kiln, 10 ports** (p.78, Fig 3-12). Ten floor burner ports of 2½ in (6.3 cm)
  diameter, about 4.9 in² (31.6 cm²) each, 49 in² (316 cm²) in all → exit flue in the arch about
  49 in² (316 cm²).
- **W5. Natural-draft flue to chimney** (p.78, Fig 3-11). Chimney 162 in² (1045 cm²) → inlet flues
  about 162 in² = four standard 9 × 4½ in (23 × 11.5 cm) flues. Fig 3-11: inlet "4 brick area 162 sq
  in" = exit flue to collection box "4 brick area 162 sq in"; entry to the chimney "3 brick area
  121.5 sq in"; chimney "4 brick area 162 sq in". The entry is 75 % of the chimney (derived).
- **W6. Draft path** (p.79, Fig 3-13). From the firebox X up the front wall, over the arch, down the
  back wall, through the flues and up the chimney to Y: 45 ft (13.7 m), "about 10 seconds" at the
  right draft (4.5 ft/s, derived). Oily-rag test: count the seconds from firebox to chimney smoke.
- **W7. Chimney height** (pp.79–80, Fig 3-14). Chamber A 5 ft (152 cm) wide, 6 ft (183 cm) to the
  crown; flue collection box B 1 ft wide; chimney C 1 ft wide. 3 × 6 ft = 18 ft ("91 x 183 = 549cm");
  horizontal pull 5 + 1 + 1 = 7 ft (213 cm) → 7 ÷ 3 = 2 ft 4 in (71 cm); chimney 20 ft 4 in, printed
  "(610cm)" (**Flagged**: 620 cm).
- **W8. Climbing-kiln chimney** (p.81, Fig 3-15). A climbing kiln on a 22° slope; the chimney top on
  the line through the chamber tops, a minimum height (Principle 8). Five or six chambers drawn; no
  dimensions.
- **W9. High altitude** (p.82, Figs 3-16, 3-17). Chimney 9 × 9 in plus 4½ in ("add 50%") → 9 × 13½ in;
  three inlet and exit flues 9 in (23 cm) high × 4½ in (11.5 cm) wide → 13½ in (34.5 cm) high × 4½ in.

### Downdraft proportions (Chapter 5)

- **W10. Early natural-draft downdraft** (pp.129–130, Fig 5-2). Chamber 6.56 ft (2 meters) wide, high
  and long (a cube); "FLUE CONNECTION 3.28 ft (1 meter)"; chimney base 3.28 ft (1 meter) diameter;
  chimney height 13.12 ft (4 meters) (faint, but 4 m is 13.12 ft: settled 2026-10-30); top "1? in" (16 in (?) by a 2½:1 taper). Caption:
  78 × 78 in (2 × 2 m) to 67 × 67 in (1.7 × 1.7 m) chambers "with the same chimney relationship".
  Text: chimney diameter half the chamber's, so it can serve more kilns, with a "greatly restricted"
  entrance flue and a 2½ to 1 taper; the chimney at 90° to the firebox flues. This height is the
  minimum, Rule 5 the maximum, which adds "an extra 1½ft (46cm)" (not reproducible from the figure's
  numbers: **Flagged**).
- **W11. Modern downdraft, 6 × 6 ft chamber** (caption Fig 5-3, p.130; figure p.131). Chimney base at
  least 12 in (30.5 cm) diameter, top 8 in (20 cm), height at least 20 ft (6 m); the chamber-to-chimney
  distance can be under 3 ft (91 cm) without changing the chimney. Fig 5-3, metric: chamber 2 m high,
  floor 2 m, flue connection 1 m, base "⅓ meter", top "20 cm", height "6 m"; imperial:
  6 ft, 6 ft, 3 ft, 12 in, 8 in, 20 ft. The figure's faint labels agree with the caption's clear
  12 in (30.5 cm), 8 in (20 cm), 20 ft (6 m) and 3 ft (91 cm) (settled 2026-10-30). Taper "1 to ¾ or 1⅓ (?) to 1"; with forced-draft
  burners up to 25 % shorter, "no certain rule" (p.131).
- **W12. Box "downward-draft" layout** (pp.150–151, Figs 5-81 to 5-84). All sides flat; burners at the
  side ("requires a bagwall"), back or floor; exit flue in the back wall at floor level. Fig 5-82:
  shelves 1–2" from the back wall, 1" apart, 3–4" front space; combustion channel 4½"; "BURNER PORTS =
  BURNER TIP SIZE"; "BURNER PORT AREA = CHIMNEY AREA". Text: channel 4½ in (11.5 cm) firing up
  through the floor; 7 to 9 in (18 to 23 cm) firing from the side or back, by burner (4½ in is enough
  with low-pressure venturi burners); a rowlock or soldier bag-wall row puts the first shelf at 4½ or
  9 in (11.5 or 23 cm). Chimney section starts equal to the burner-port area; height equal to the
  kiln's, or level with the top of the frame, with a hood and stack above; exit-flue width equal to
  the chimney's, then restricted with a brick.

### Updraft layout and frame (Chapter 6)

- **W13. Small atmospheric-burner updraft** (pp.171–173, Figs 6-63, 6-65 to 6-67). "A 2, 3 or 4cu.
  (0.06, 0.08, or 0.11cu. m) cube (in terms of the amount of stacking space)" with "a 1½in. (4cm)-rise
  number 1 arch" (**Flagged**: Fig 6-63 draws a 3–4' cube, and six burners suit 21–32 ft³, derived;
  the arch is presumably 1½ in per ft). At most six atmospheric burners plus one optional bottom
  burner, each 35,000 to 54,000 BTU/hr (printed "10.26 to 15.83Kwh": **Flagged**, kW); or three per
  side in channels. Combustion space at least 4½ in (11.5 cm) for 2½–3 in tips; 6 in (15 cm) for a 4 in
  tip; up to 9 in (23 cm) for tempered-air blocks. Perimeter burners 6–12 in from the corners and 9–12
  in apart (text p.171); the caption says "9 to 12in. … from the corners, and 12 to 24in. … apart"
  (the two disagree). Side-channel burners 1–6 in from the corners, then 9–12 in apart. Drawing:
  perimeter burners at 10", 12", 10"; side burners in 4½" channels at 6", 12", 12", 6"; back-wall
  circulation 2–4½". Bottom burners: at least 2½ in between the setter shelf and the floor; an "S"
  support layout with one bottom burner for 12 × 24 or 12 × 18 in shelves, an "X" layout otherwise.
  Floor ports 2½–2¾" for a 2½" tip, the tip at least ¼" below the floor; floors 4½–5" thick (Fig
  6-67). Side ports 4½ × 5 in for one burner, 4½ × 9 in for two (p.173).
- **W14. Frame for an updraft 5 × 5 × 6 ft outside** (p.174, Fig 6-69; `kiln-reference.md` §2):
  corners 3 × 3 × ¼ in angle; top and bottom ties 2 × 2 × ¼; floor perimeter 4 × 4 × ¼; floor joists
  2 × 2 × ¼; door frame 3 × 3 × ¼; skewback brace 2 × 2 × ¼. The figure's caption says "4 x 4ft (122 x
  122cm) kiln" (**Flagged**: the text says 5 × 5 × 6 ft).

### Gas burners and orifices (Chapter 8)

- **W15. 36 ft³ IFB updraft** (p.226): "will have a minimum of 10 such burners" (36,000 BTU/hr each)
  and will fire easily in 8 h. 10,000 BTU/ft³/hr (derived). Overpowering only shortens the firing.
- **W16. 20 ft³ IFB cross-draft on natural gas** (pp.227–228), "maximum figures": 20 × 10,000 =
  200,000 BTU/hr; four burners (simple air mixer with flame tube) at 50,000 BTU/hr each; Rule 4,
  9.1 × 20 = 182 CF/hr, 45 CF/hr per burner; at 8 in. WC the gas-flow chart gives orifice **#34** (the
  text cites "Fig. 8-44"; the chart is Fig 8-39). A home meter gives 175 CF/hr, 7 short, so no water
  heater or range while firing. At the 7000 BTU minimum the kiln draws 128 CF/hr, leaving 47 CF/hr,
  enough for a 40-gallon water heater only. The 150,000 BTU per 9 ft³ rule would call for over
  300,000 BTU/hr. The note's check: Ward's #34 at 8 in. WC is 45,312 BTU/hr, about 45 CF/hr.
- **W17. Flame safeguard cost** (p.240): a "normal" 50 ft³ (1.42 m³) downdraft would need about
  $3500 / £2188 or more for TFM or UVM parts and installation.
- **W18. Burner set-ups drawn** (no kiln sizes): Fig 8-56 (p.229), cross-draft and downdraft, three
  burners per side, each controlled; Fig 8-62 (p.237), LP tank → regulator 0–30 psi → ¾" buried black
  pipe → WC regulator → three burners; Fig 8-64 (p.238), three side-wall burners on one valve with
  safety shut-off and pilot; Fig 8-64A (p.239), three MR-750 burners on a 4-way tee with a Baso
  H15DA-1 ¾" safety valve and a continuous match line; Fig 8-65 (p.239), the updraft floor-burner
  safety system.
- **W19. Burners and orifices:**
  - Gas-flow chart sample (p.217, Fig 8-39): 8 in. WC and 30,000 BTU/hr → No. 44 drill.
  - Gas Appliance simple atmospheric mixer (pp.220–221, Fig 8-40): flame tube 2 in (5 cm) black pipe,
    8 in (20 cm) long; 9 in (23 cm) orifice to tip; at least ½ in (1.3 cm) between mixer and shutter.
    Natural gas No. 32 → 54,000 BTU/hr at 8 in. WC; propane No. 45 → 50,000 BTU/hr at 11 in. WC;
    butane No. 46 → 57,200 BTU/hr at 11 in. WC.
  - Gas Appliance MR-750 (p.221, Fig 8-41): rated 75,000 BTU; range 17,490 to 78,440 BTU up to 9.5 in.
    WC (lower pressure lost in the gutter). MR-750 and MR-100: 75,000 and 100,000 BTU/hr at 8 in. WC
    (p.222).
  - Danish propane weed burner (p.222, Fig 8-44): mixer and intensifier ⅝ in (1.6 cm) from the lip; 11
    holes; about 1¼" diameter, 2½" tall (drawing).
  - Eclipse standard injector (p.222), for 530–1200 BTU/ft³ gas: on natural gas at most 7 in. WC, a
    2 in (5 cm) outlet passes 83 CF/hr = 91,300 BTU/hr, a 3 in (7.5 cm) outlet 185 ft³ (5.24 m³)/hr =
    203,500 BTU/hr. Compound injector: 1200–3300 BTU/ft³ gas (p.224).
  - Polidoro tubular burner (p.223, Fig 8-46): stainless tube 24½" long; venturi 7½" long (printed "7½" ID"; Checked on the page image, 2026-10-31),
    1 5/16" I.D.; deflector 1⅛"; 3" from the orifice bracket.
  - Rohde pot burner (p.223): kilns up to 2552 °F / 1400 °C; 20 kW = 68,242 BTU; 0 to 1.5 bar of
    propane.
  - Eclipse TA-53 tempered-air burner (p.224): 100,000 BTU/hr maximum, 20,000 minimum, natural gas at
    5 in. WC.
  - Alfred pipe burner (p.225, Figs 8-51, 8-52): 2" pipe 8–10" long; outlet beyond the elbow at least
    3 × the pipe size; 1½–2" pipe best; at 11 in. WC an 11/64" orifice gives 202,400 BTU/hr; a No. 32
    "73,600" (?, second digit unclear). The note's check against Table 8-7: about 206,000 for 11/64"
    (agrees), 94,000 for #32 (doesn't).
  - Forced-air pipe burner (p.225, Fig 8-53): "3" pipe burner needs 2850–3300 RP[M] 115V 50/60 C[ycle]
    ¼ HP motor – 2" × 5" impeller"; the drawn unit 1600 RPM, 1¾" × 3¾" impeller, 2" pipes.
  - Simple pipe burner, Table 8-8 (p.226): flame tube 2" / 1½" / 1¼"; tube 7–8"; manifold 1¼" / 1" /
    ¾"; orifice 30 / 32 / 39; about 40,000 / 54,000 / 60,000 BTU. **Flagged**: the #30 and #39 ratings
    look swapped (#30 is about 66,000 by the orifice equation, #39 about 40,000).
  - Ward's tables (pp.230, 232): natural gas #38 at 7 in. WC = 35,423.95 BTU/hr; 125,000 BTU at 7 in.
    → #11 (37,932.60); Atlanta (1050 ft), #28 at 8 in. = 71,413.84 BTU/hr. Propane #38 at 11 in. WC =
    71,989.71 BTU/hr; 125,000 BTU at 1 psi → #36 (29,492.10 orifice function); Atlanta, #38 at 11 in.
    = 70,902.66.
  - Regulator (p.236): meter at 2 psi, burners at 8 in. WC, a 1 in (2.5 cm) line and 500 CF/hr → a
    Maxitrol 325-5 with an E (HO-1) spring; inlet up to 25 psi, outlet 2 in. WC to 3 psi, 675 CF/hr.

### Oil (Chapter 8)

- **W20. 50 ft³ oil kiln with two opposed burners** (p.214): 50 ft³ (1.42 m³) × 10,000 BTU (IFB) or
  16,000 BTU (firebrick) ÷ 2 burners. Not finished in the book: 250,000 or 400,000 BTU/hr per burner
  (derived).
- **W21. 924,000 BTU/hr oil kiln** (p.212; Table 8-4, p.214): two forced-oil/air burners on three-stage
  adaptors; each: nozzle #1 0.5 GPH (66,000 BTU/hr), #2 1.0 GPH (132,000), #3 2.0 GPH (264,000); 3.5 GPH,
  462,000 BTU/hr per burner; two give 924,000 BTU (271 kW). Sequence: #1 alone 0 to 1000 °F (538 °C);
  #1 + #2 printed "1000–1060°F (538–1016°C)" (**Flagged**: 1000–1860 °F is meant); all three from
  1850 °F (1016 °C). Six turn-up combinations printed; the text says seven (#3 + #2 is missing).
- **W22. Forced-oil/air burner** (p.211, Fig 8-28): 5 GPH × 132,000 BTU/gal = 660,000 BTU/hr; its air
  need is lost in the gutter ("...00 CFH"). A 3 GPH nozzle gives 2.7 GPH at 80 psi and 3.43 GPH at
  130 psi; a hot nozzle flows about 6 % less. Drawing: motor ⅛ HP, 1725 RPM; ignition transformer
  10,000 V; nozzle 5–8" long; pump 100–150 psi.
- **W23. Alternate oil-drip unit** (p.209, Fig 8-22): two drip plates in a 6 in (15 cm) channel iron set
  in the flue channel; side 14" long × 12" high (the front view's height also reads 12": Checked on the page image,
  2026-10-31); front 6" wide. Carbon is hard to clean, the iron
  burns away, the plates are too small; good only for pre-firing.

### Electric (Chapter 9)

- **W24. Kilowatts for a 2 × 2 × 2 ft kiln** (p.256, Fig 9-27): "2 x 2 x 2ft = 8ft" (8 ft³). By
  volume: 8 × 1.5 kW/ft³ = 12 kW (low), 8 × 2.07 = 16.5 kW (high). By wall area: 24 × 24 in = 576 in²;
  × 4 walls = 2304 in²; × 5 W/in² = 11.5 kW (low), × 7 = 16.1 kW (high). Fig 9-27 draws five squares
  but the example counts four walls. By Table 9-6, 16 kW is too high; "the lower values fall in the
  middle".
- **W25. Element design, 10½ ft³, cone 10** (pp.258–260): "10½CF"; 240 V, 108 A, 26 kW; "Six element
  groups and six switches"; 108 ÷ 6 = 18 A per group; "4333W output per group". Surface load chosen
  p = 8 W/in² (from 6.4–9); Ct = 1.04. Quick method printed "18 x 1.04 / 8" = 42.12 in²/Ω (the square
  is missing: Flagged in `kiln-reference.md`) → B&S 10. Ohm's law: Rh = 240² ÷ 4333 = 57600 ÷ 4333 =
  13.3 Ω hot; Rc = 13.3 ÷ 1.04 = 12.8 Ω cold. Check printed "4333 / 8 x 12.2 = 4333 / 102.4 = 42.4"
  (**Flagged**: 12.2 for 12.8). Wire B&S 10, d = 0.102 in, 0.083 Ω/ft used; L = 12.8 ÷ 0.083 = 154.2 ft
  per group. Actual load printed 7.4 W/in² (the denominator 582 should be about 593, giving 7.3:
  derived). Coil D = 5–6 × d "for temperatures exceeding 1830°F (999°C)": 0.51 to 0.612 in; 9/16 in
  (0.56) used. Turns: 154.2 × 12 ÷ (3.14 × (0.56 − 0.102)) = 1850.4 ÷ 1.43 = 1293. Close-wound
  1293 × 0.102 = 131.8 in (10.98 ft). Stretched at pitch 2d (printed "S (pitch) = 20"): 263.6 in, "or
  22ft (approximate)". The same kiln is the 26.000 kW row of Table 9-6. 2.48 kW/ft³ (derived).
- **W26. Kanthal nomogram** (p.261, Fig 9-29): two worked traces, I and II; their values are
  unreadable in the scan.
- **W27. Lid vents** (p.249, Fig 9-20): a top-loader lid 22 × 52 in (56 × 132 cm) with one vent 2½ × 2½
  in (6.3 × 6.3 cm) in each half, on the centre line. Any kiln over 8 ft³ needs a roof vent.

### Walls

- **W28. 7 in fibre wall against 7 in IFB wall** (p.39, Table 1-12), both at a 2350 °F (1288 °C) hot
  face: fibre (4 in Cerablanket + 3 in "FB? 1900" block (labels faint)): cold face 248 °F (120 °C),
  storage 1941.85 BTU/ft², loss 446.74 BTU/ft²·h. IFB (4½ in K-26 + 2½ in K-23): cold face 227 °F
  (109 °C), storage 8674.6 BTU/ft², loss 360.19 BTU/ft²·h. Ambient and method not stated.
- **W29. IFB corner in a steel frame** (p.52, Fig 2-32): K-26 IFB stretchers backed by a K-20 rowlock
  course (7 in); sheet-metal side, angle-iron corner post; a ¼ in fibre pad mortared to the brick end;
  "¼" expansion joints used when walls are greater than 48" in length".
- **W30. Three 7 in electric-kiln walls** (p.248, Fig 9-16, "NOT TO SCALE"): (1) 4 in (10 cm)
  high-temperature M-Board (grooved hot face), 2 in (5 cm) low-temperature board, 1 in (2.5 cm) dead
  air, louvred shell; (2) a grooved IFB stretcher course backed by 2½ in (6.3 cm) block insulation,
  metal case; (3) a stretcher course backed by a K-20 rowlock course, metal case. Element rows 2½ in
  apart.
- **W31. Round kiln proportion** (p.75, Fig 3-4): a dome in a cube, d and h marked, beside a square
  elevation 6' wide × 6' high (drawing): diameter and height "nearly equal".

---

## 12. Table 9-6: 28 manufactured electric kilns (p.257)

"Kilowatt power calculations", compiled by Olsen "using manufactured kilns available on the market
in 2010" (p.256). No makes or models are named. The page curve hides the left edge: volumes marked
(?) are partly cut, and each row was traced along its grid line to place the "Elements Required"
cell. kW/ft³ is derived. kW = V × A holds for every single-phase row except the two flagged below.

| Volume ft³ | kW | Volts | Amps | Elements | kW/ft³ (derived) |
|---|---|---|---|---|---|
| 1 (?) | 1.800 | 120 | 15 | – | 1.80 |
| 2 (?) | 4.600 | 230 | 20 | 3 | 2.30 |
| 2 (?) | 5.500 | 220/240 | 25 | 3 | 2.75 |
| 2 (?) | 4.600 | 230/208 | 20 (three-phase) | 3 | 2.30 |
| 3 | 5.290 | 230 | 23 | 4 | 1.76 |
| 3 | 5.060 | 230 | 22 | 4 | 1.69 |
| 3 | 5.760 | 240 | 24 | 4 | 1.92 |
| 4 | 8.050 | 230 | 35 | – | 2.01 |
| 4 | 11.000 | 208/240 | 26.6 (three-phase) | – | 2.75 |
| 4 | 10.800 | 240 | 45 | – | 2.70 |
| 5 | 14.400 | 220/240 | 60 | – | 2.88 |
| 5 | 8.850 | 230 | 38.5 | – | 1.77 |
| 5 | 7.800 | 230 | 34 | – | 1.56 |
| 6 | 9.200 | 230 | 40 | 5 | 1.53 |
| 7 | 16.800 | 220/240 | 70 | – | 2.40 |
| 7 | 11.250 | 230 | 47 | – | 1.61 |
| 8 | 14.400 | 220/240 | 60 | – | 1.80 |
| 8 | 10.350 | 230 | 45 | 5 | 1.29 |
| 8 | 9.200 | 230 | 40 | 5 | 1.15 |
| 10 | 13.800 | 230 | 60 | 6 | 1.38 |
| 10 | 26.000 | 240 | 108 | – | 2.60 |
| 13 | 30.000 | 220/240 | 125 | – | 2.31 |
| 13 | 24.000 | 220/240 | 100 | – | 1.85 |
| 13 | 25.000 | 220/240 | 75 | (blank) | 1.92 |
| 15 | 34.500 | 230 | 150 | 6 | 2.30 |
| 16 | 36.000 | 220/240 | 150 | – | 2.25 |
| 16 | 30.000 | 220/240 | 125 | – | 1.88 |
| 16 | 24.000 | 240 | 100 | 5 | 1.50 |

- **Flagged**: 11.250 kW at 230 V × 47 A is 10.81 kW (240 V gives 11.28); 25.000 kW at 220/240 V ×
  75 A fits neither single phase (18.0 kW at 240 V) nor three phase (31.2 kW) (derived).
- The 26.000 kW, 240 V, 108 A row is the 10½ ft³ kiln of worked example W25, placed in the 10 ft³
  group.
- Range 1.15–2.88 kW/ft³, median about 1.9 (derived).

---

## 13. Kilns that can't be modelled

The 33 kilns marked **none**: the book doesn't fix the chamber's size.

- `olsen-kit-36`: model name and two photos only.
- `olsen-fiber-p62`: firing schedule and anchor failure only; no fuel, draft or size.
- `bailey`: maker and a photo only.
- `job-forni-gas`: no size; only its burner is drawn.
- `fast-fire-kecskemet`: a shelf failure and the door type only.
- `fast-fire-cappadocia`: 9 in walls only; its sizes were set by shelves the book doesn't size.
- `hacettepe-2004`: named only.
- `finch-fast-fire`: layout described, no dimension.
- `salzer-phoenix`: layout described, no dimension.
- `olsen-first-kiln`: no dimensions printed (the revised design is `bowen-mountain`).
- `kyomizu`: chamber count and one uncertain label, "4' INSIDE" (?).
- `onda-koishibara`: a proportion only (width about equal to height).
- `kanayama-bizen`: firing practice only.
- `olsen-chamber-p23`: shelf size and arch movement only.
- `hart-square`: only a width, derived from the chimney columns; the drawing is illegible.
- `hohr-2003`: no dimension in feet or inches; shelf count uncertain.
- `olsen-anagama-p26`: hot-face material only.
- `bayer-tube-form`: a photo of a form only.
- `baobab`: a type; drawing labels only.
- `greek-updraft`: a type; drawing labels only.
- `bottger`: layout only.
- `bottle-two-storey`: a type; only the dome's "2' or more".
- `sevres`: photos only.
- `milton`: named only.
- `kecskemet-multi`: fire zone only "larger" than 9 ft.
- `kanayama-multi`: fire zone set by 16 shelves of unstated size; fireboxes, walls and dome are known.
- `jiesia`: photos only.
- `job-forni-hobbyker`: wall build only; no chamber size or power.
- `electric-reduction-smoke`: flue and firebox sizes only; no chamber size or power.
- `kanayama-oil`: 7 in firebox and walls and a 9 × 9 in chimney; the plan was set by shelves the book
  doesn't size.
- `leach-chamber`: its outside oil fireboxes only.
- `park-tuscarora`: firebox width and burner only.
- `soldner-raku`: burner only.

Also not modelled: the kilns named only, listed under the index (Soldner's catenary, the Minnesota
Flat Top, Geil, Rohde, Nabertherm, the corbel-arched kilns, Chien Yao, Seto, Cassel, Newcastle and
Burlon Craig's kiln).


## Unclear figures read again (2026-10-31)

Each read on the page image (`kiln-reference.pdf`, 110–600 dpi). Settled rows are marked
Checked on the page image, 2026-10-31, where they appear above.

| Kiln, figure, page | Was | Reading | Settled? |
|---|---|---|---|
| Kato, Fig 5-4, p.131 | walls "10"" (?) at the door end and by the chimney | "10"" at both | yes |
| Kato, Fig 5-4, p.131 | "TAPERING TO 15½"" (?) | "15½"" | yes |
| Kato, Fig 5-4, p.131 | "30"" (?) at the outer wall | "30"" | yes |
| Kato, Fig 5-4, p.131 | length "7'" | the digit runs under an arrowhead | 7 ft, read by the user, 2026-10-31 |
| Moveros, Fig 6-3, p.153 | mouth 22" (?) wide, maybe 28" | "22"" | yes |
| Miravet, Fig 6-19, p.158 | 6' to where the dome starts (?) | the 6' arrow ends at the dome's lower edge | yes |
| Miravet, Fig 6-19, p.158 | 3' from the mouth sill down (?) | the 3' arrow runs down from the 27" mouth | yes |
| Singh low-fire, Fig 6-12, p.156 | 2' below the ground line (?); 2'6" dome to pit floor (?) | both arrows end on the pit floor; 2' from the ground line, 2'6" from the domed floor's underside | yes |
| Singh low-fire, Fig 6-12, p.156 | side opening | washed out at 600 dpi | 12–15 in, the side entrance from the firebox, read by the user, 2026-10-31 |
| Singh coal, Fig 5-10, p.134 | chimney height | washed out at 500 dpi | 30 ft tall, about 25–30 ft from the chamber, read by the user, 2026-10-31 |
| Singh coal, Fig 5-11, p.134 | "STOKING HOLE 15" X 1?"" ; "AIR SOURCE … 36" X 24"" (?) | not legible at 600 dpi | 15 × 13 in, read by the user, 2026-10-31; the ash pit stays (?) |
| Bowen Mountain, Fig 4-153, p.127 | arch down to 18" (?) at the back | "18"" | yes |
| Bowen Mountain, Fig 4-153, p.127 | firebox 12" (?) below the floor | "12"" | yes |
| Bowen Mountain, Fig 4-153, p.127 | three (?) inlet flues across the front | four openings drawn in the plan's front wall | yes: `bowen-mountain.yaml` goes from 6 to 8 burners |
| Bowen Mountain, Fig 4-153, p.127 | "4½" X 7" FLUES" | "7"" reads clearly; the block is drawn 9" × 4½" | 4½ × 9 in, as drawn: the 7 a misprint, read by the user, 2026-10-31 |
| Chappell, Fig 4-149, p.126 | second chamber "5½' TALL" | "5'½" TALL" faint | 5½ ft, read by the user, 2026-10-31 |
