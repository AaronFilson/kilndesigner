# Olsen's kilns

The kilns Frederick L. Olsen describes in *The Kiln Book* (4th ed.), as design files: every one whose
chamber the book sizes. They were built and fired, so the engine must build each one without an
error, and `core/tests/test_olsen_kilns.py` builds them all (ADR 0014). A warning that stays must be
true of the kiln as built; the test lists each with why.

The numbers come from `docs/research/olsen-kilns.md`, which cites the book's pages. Each file's
header says three things: what the book gives, with its page or figure; what had to be assumed,
and from where (an Olsen rule, or a related kiln named by its file); and what the engine can't
represent and how the file approximates it. Values the book prints as uncertain, or as misprints,
are marked so there too.

## The kilns

Gas updrafts and box kilns: `olsen-kit-16`, `olsen-kit-24`, `olsen-kit-50` (a car kiln),
`olsen-kit-100`, `kaneko-car`, `updraft-test-1` to `updraft-test-4` (the kilns behind Olsen's
first design principle), `olsen-crossdraft-36`.

Downdrafts: `kahler-salt`, `blakebrough-tasmania` (fibre), `fast-fire`, `fast-fire-anderson`,
`phoenix-nh` and `phoenix-wright` (only their volume and layout are printed; the rest is Olsen's
rules), `bowen-mountain`.

Chamber and climbing kilns: `bidai`, `kawaii`, `kyoto-climbing` (the type), `suzuki-kyoto`, `tobe`,
`fujiwara-bizen`, `kitade-tojilo`, `blakebrough-sturt`, `olsen-two-chamber`,
`olsen-three-chamber` (gas), `chappell-domura` (its salt chamber), `hotchkiss-raw-clay` (raw clay
fired in place).

Tube, groundhog and tunnel kilns: `groundhog-basic` (the type), `meaders-cheever`, `meaders-david`,
`ellington-new-hog`, `bae-gilgama`, `tamba`, `la-borne`, `kannofen`, `conrad-teardrop`,
`hollyweird`, `anagama-hole` (dug into a clay hill).

Multi-directional kilns: `fireworks-edmonton`, `church-skaelskor`.

Round, bottle and folk kilns: `moveros-umbrella` (granite), `ninodaguia` (common brick),
`singh-lowfire`, `miravet`, `falcone-pompeii`, `kenzan-muffle`, `breda-bottle`.

Fifty-three kilns in all. Where the book names no grade of firebrick, the files take medium-duty
brick, the intermediate duty Olsen gives potters' kilns to about cone 10 (p.18); floors that roof a
firebox take super-duty. Raw clay fired in place (Hotchkiss's blocks, the anagama's clay bank) is
taken as porous fireclay brick, between low- and medium-duty brick, as the user judged and
`docs/research/masonry-materials.md` §4a supports; the raw clay behind the fired skin isn't
modelled.

Coal and oil: `kato-coal`, `singh-coal`, `olsen-oil-drip`.

Electric: `electric-car-45`.

## Not modelled

- The 33 kilns whose chamber the book doesn't size (a name, a photo, a firing log or one part):
  `docs/research/olsen-kilns.md` §13 lists each with what it gives.
- `gulgong-racer`: its dome is Moral Coolcast 140 (Morgan's 140MW, a medium-weight insulating
  castable), for which no technical data sheet was found; its safety data sheet gives no thermal
  data (`docs/research/masonry-materials.md` §5.4).
- `pit-kiln-improved`: its fuel burns among the ware, with no firebox, which the engine can't model;
  its base is printed "4'12"".
- The book's pages that aren't in the scan (pp.1–14, 190–193, 195 and 263–294, the experimental
  kilns), left out by the user's decision.

## What the engine approximates

- Chambers in a row are all one size: the mean, or the largest, as each header says.
- A chamber kiln's arches span each chamber along the draft and rest on the common walls; the
  engine's arch spans the width, so these kilns' arches are taken as held by masonry
  (`buttressed`) and get no steel.
- Teardrop, tapering and multi-directional plans are boxes of the mean width.
- One exit flue, one chimney and one stoke hole per firebox; one fuel per kiln.
- A floor on the ground (`chamber.on_ground`) or over its fireboxes isn't counted in the heat loss.
