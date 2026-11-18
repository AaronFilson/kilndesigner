# Page images and questions for engine v2 (2026-11-17)

A handoff for a session in another local repo. The owner thinks that repo's `scratch/` folder has
scans of Olsen's *The Kiln Book* (4th ed.), but isn't sure which folder. The details behind each
item are in [11-17-26-inputs.md](11-17-26-inputs.md); the section numbers below are that file's.

## 1. Find the page images

Look for scans of the pages below. The folder that has them is the one this work needs.

| For | Kiln (design file) | Pages | Figures |
|---|---|---|---|
| Principle 6 chimney and flue sizes (§1) | Anagama in the hole (`anagama-hole`) | 83–84 | 4-5 |
| | Falcone (`falcone-pompeii`) | 160–161 | 6-32, 6-34 |
| | Fireworks (`fireworks-edmonton`) | 178–183 | 7-1 to 7-7 |
| | Kannofen (`kannofen`) | 161–164 | 6-37, 6-39 |
| | La Borne (`la-borne`) | 109–111 | 4-78 to 4-80 |
| | Kitade (`kitade-tojilo`) | 202 | 8-11 |
| Tamba's slope and arches (§9) | Tamba (`tamba`) | 85–88 | 4-7, 4-17; also 4-11 to 4-16 |
| Side stoke holes and air inlets (§3, optional) | Suzuki | 93 | 4-35 |
| | Kyoto | 89–94 | 4-28, 4-31 to 4-34 |
| | Bidai | 94–97, 200–201 | 4-36, 4-37, 8-7 |
| | Kawaii | 97, 200 | 4-45 to 4-48 |
| | Hotchkiss | 54–57 | 2-39 to 2-46 |
| | Hollyweird | 116–117 | 4-108, 4-110 |
| | Olsen's general text on stoke holes | 199–206 | 8-7 |

## 2. What to read from them

- **Principle 6 (§1):** for each of the six kilns, the chimney's section and the exit flues.
  - Where the drawing shows them to a scale, scale them. Record the page, the figure, the scale
    and ±1 scaled unit.
  - Where the drawing doesn't show them, write "not shown". The engine then uses Principle 6's
    large side, ¼ of the chamber's width.
- **Tamba (§9):**
  - the floor's rise over its run, on Fig 4-7 and on Fig 4-17. If the two disagree, give both;
    they become the band's ends;
  - the supporting arches that narrow the tube into semi-chambers, one at the back of each,
    before the next side stoke hole: each arch's opening (width and height) and its spacing.
- **Side holes and inlets (§3):**
  - any side hole's size, from a scale or the text;
  - above all, any separate air inlet for a chamber that isn't its stoke hole. Stoke holes are
    covered after stoking.
  - pp.199–206: whether Olsen gives a typical side-hole size.

## 3. Getting them back here

Reads outside `/home/bellows/kilndesigner` are blocked. Either copy the images into
`/home/bellows/kilndesigner/scratch/olsen-pages/` (git-ignored; name them by page, such as
`p085.png`), or record the scaled numbers in a file this repo can read. Don't commit the scans to
either repo: they are the book's pages.

## 4. Questions for the owner, still open

1. **Singh's shard cover (§4):** is a band from a single thin layer to 4 in thick right? How open
   is it, roughly? No source gives either.
2. **Kitade's second chamber (§8):** the book draws only the first. May the second be taken as
   the same size and slope?
3. **Separate side air inlets (§3):** the known ones are:
   - Bidai's air and stoke opening (Fig 8-7);
   - Hollyweird's air holes at grate level;
   - the two openings at the base of Kitade's firebox.
   Do Suzuki, Kyoto, Tobe, Kawaii, Hotchkiss or Fujiwara have any?
4. **The fire mouth, by kiln (§2):** which kilns are fired with the mouth open, and which are
   covered for slow cooling? Without an answer, v2 reports each kiln in all three states.

## Answered today (for reference)

All recorded in [11-17-26-inputs.md](11-17-26-inputs.md):
- Principle 6: scale from the drawing, or take ¼ of the width.
- The fire mouth: open, partly open or closed, set per stage.
- Stoke holes: covered after stoking; a bundle-stoked hole is at least 16 in.
- Hollyweird's side door: 9 × 13½ in.
- Kitade's p.202 hole: 9 × 7 in.
- Singh: the top is under 2100 °F; the cover is porous shards.
- Breda: the setting is a band, about 10 h, 1800 kg of wood, the top up to cone 2.
- The 36 ft³ cross-draft: an example of a principle.
- Kähler and Blakebrough: Rule 1 bands.
- Kitade: 2 chambers, the chimney by Principle 6.
- Olsen's two-chamber design: unbuilt, out of the reference set.
- Tamba: one tube, its arches making semi-chambers; the slope from Figs 4-7 and 4-17.
- Suzuki's chambers 4–7: 60 bundles a side over 5 h.
- The lower-bound rule: yes.
- IFB emissivity: keep the extrapolation.
