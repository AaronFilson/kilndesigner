# Kähler salt kiln, Næstved (`kahler-salt`)

Nils and Herman Kähler's 16 cu ft gas downdraft salt kiln, side-fired by four forced-air burners
staggered so the flame rolls round the chamber. Design file: `examples/olsen/kahler-salt.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.136 (text; Figs 5-17 front section, 5-18 side section, 5-19
flame path, 5-20 and 5-21 photos), p.137 (text). Notes: `docs/research/olsen-kilns.md`.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 30 in wide, 48 in to the arch line, 36 in deep (Figs 5-17, 5-18) | 30 × 36 × 48 in | matches |
| Walls | 7½ in high-alumina IFB | 7½ in JM 28 | matches |
| Arch | sprung, size not printed | 4½ in JM 28, 1½ in/ft | assumed |
| Burners | four forced air/gas; left wall 18 and 39 in up, toward the front; right wall 9 and 28 in up, toward the back (Figs 5-17, 5-19) | four power burners at those heights, 12 in off centre toward the front (left) and back (right), by scale (drawing)(?) | matches; across positions read off the drawing |
| Burner ports | K28 dense port blocks, size not printed | 4½ × 5 in, Olsen's side port (p.173) | assumed |
| Spy holes | three "SPY AND DRAW HOLES" up the door (Fig 5-18) | three in the front wall, 13, 25 and 37 in up (drawing)(?) | matches; size engine default |
| Door | in the end ("DOOR", Fig 5-18); hung steel door with latches (Fig 5-21) | whole front wall, hinged | matches; door size not printed |
| Exit flues | three 4½ × 9 in floor flues into collection channels 4½ × 9 in (Figs 5-17, 5-18) | three 4½ × 9 in floor flues, spread evenly (`draft.exits`) | matches the flues (places not printed); the channels aren't modelled |
| Chimney | flue 9 × 7 in max through the crown, 10–12 ft tall | 9 × 7 in, 11 ft, through the crown (`draft.chimney_through: crown`) | matches |
| Salt ports | top front and top back, in the arch | — | expressible (`openings.salt_ports`), but their size isn't printed |
| Floor slab | 4½ in clear of the walls | — | not expressible |

## Key results (engine build)

Chamber 31.6 ft³ (the 16 cu ft is stacking); heat loss at top 16.4 kW; design input 315,625
BTU/hr on four Ward MB200 power burners; chimney draft 0.10 in. w.c. with gas at 1000 °F; arch
frame L4×4×¼ with ½ in rods.

## Open questions for the user

1. Fig 5-18: are the left-wall burners about 4 in from the door-end wall and the right-wall
   burners about 4 in from the back wall, as read by scale?
2. Fig 5-18: are the three spy and draw holes about 13, 25 and 37 in above the floor?
3. Fig 5-18 "40½"": what does it measure?
