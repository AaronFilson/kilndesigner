# Olsen's three-chamber climbing kiln (`olsen-three-chamber`)

Three gas-fired chambers of 120 cu ft on six Eclipse TR-80 compound injectors. Design file:
`examples/olsen/olsen-three-chamber.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.224 (text only). No figure.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chambers | three of 120 ft³ | three 59.2 in cubes | assumed shape |
| Burners | six TR-80, about 214,200 BTU/hr each at 10 in. w.c. | six at that rating, propane line at 10 in. w.c. | matches; positions not printed |
| Slope, walls, arch, flues, chimney | not printed | see the design file | assumed |
| Doors, spy holes | not printed | engine default | — |

No change in this pass.

## Key results

447 ft³ (Ward's way, all three chambers); heat loss 48.6 kW; Ward's input 4.4 million BTU/hr
against the 1.29 million printed (the engine fires all three chambers at once, a climbing kiln
doesn't); chimney 7.3 ft by the engine.

## Open questions for the user

1. Where were the six burners: two per chamber, or all in the first?
</content>
