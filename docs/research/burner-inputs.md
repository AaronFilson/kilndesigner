# The reference gas kilns' burners at their supply pressure

Research for part C2 of the round of 2026-11-10 (`docs/planning/11-10-26.md` §C), for ADR 0017
decision 13: "Burners are sized, not assumed ... the engine picks the burner that sizes best from
the burner charts, the spacing and the gas system." What each gas kiln's printed burners give at
their printed (or the design's) supply pressure, from the charts the engine holds, against what a
firing needs. The code is `kilndesigner.v2.heat.burners` (`design_input`, `orifice`); the tests
`core/tests/v2/test_heat_burner_inputs.py` and `test_heat_gas_electric.py`.

Olsen is *The Kiln Book*, 4th ed., cited by its printed page. Marks: **Read**, **Derived**.
Worked 2026-11-10.

## 1. The charts (Read)

- **Venturi burners on one orifice** (`data/gas.yaml`, `combustion-and-masonry.md` §3.2 [S27]):
  Ward's published propane ratings by pressure, the MR-750's and MR-100's from 2 psi up on the
  √pressure curve; their 11 in. w.c. ratings (72,000 and 94,000 BTU/hr) a low-pressure orifice of
  their own (about twice the curve's). On natural gas, Olsen's 75,000 and 100,000 BTU/hr at 8 in.
  w.c. (p.222). Through one orifice the output goes as √pressure (p.216), carried for natural gas
  only within low pressure, 11 in. w.c. (p.215).
- **Olsen's orifice equation** (p.216): Q = 1658.5·K·A·√(ΔP/d) ft³/hr, A in in², ΔP in in. w.c., d
  the gas's specific gravity, K 0.80 for good atmospheric orifices; × the gas's heating value. Ward's
  tables (Tables 8-11 to 8-14, pp.230–233) are this at K 0.80 on natural gas at 1,000 BTU/ft³, SG
  0.64; Table 8-7 (pp.218–219) on propane at 2,500 BTU/ft³, SG 1.53 and butane at 3,175, SG 2.00;
  the gas-flow chart (Fig 8-39, p.217) on natural gas at 1,100 BTU/ft³, SG 0.65
  (`kiln-reference.md`, Orifices). Low pressure only (`combustion-and-masonry.md` §3.4).

## 2. Number drills (standard sizes)

The orifices the book prints are number drills: #18 0.1695 in, #32 0.1160 in, #34 0.1110 in, #38
0.1015 in, #45 0.0820 in, #46 0.0810 in, #50 0.0700 in (ASME B94.11M's standard sizes; #50 and #55
are in `combustion-and-masonry.md` §3.4). Check (Derived): Ward's printed orifice function for #38,
10,711.16 = 1.324 × 10⁶ × its area (Table 8-12, p.231), gives 0.1015 in.

Checks of the equation against the book's own figures (Derived; `test_heat_burner_inputs.py`):
Ward's #38 at 7 in. w.c. on natural gas, 35,424 BTU/hr (p.230); his propane #38 at 11 in., 71,990
(p.232); Gas Appliance's #32 on natural gas at 8 in., 54,000 (p.220–221, on Fig 8-39's basis);
a #18 at 10 in. w.c., 191,000 on propane and 211,700 on butane (`olsen-kilns.md`, the three-chamber
kiln's note): each within 0.5 %, butane's within 1 %.

## 3. Each kiln's burners at its pressure (Derived)

| Kiln | Burners (page) | Gas and pressure | Each (BTU/hr) | All (BTU/hr) |
|---|---|---|---|---|
| olsen-kit-24 | 10 (p.174), MR-750 or MR-100 (p.222) | natural gas, 8 in. w.c. (assumed, p.227) | 75,000 or 100,000 | 750,000 or 1,000,000 |
| olsen-kit-24, p.221's firing | the #32 natural-gas orifices kept on propane | propane at most 4 in. w.c. (printed) | 56,700 (orifice equation) | 567,000 |
| olsen-three-chamber | 6 Eclipse TR-80s on #18s (p.224) | LP at 10 in. w.c. (printed) | 214,200 printed; #18 gives 191,300 on propane, 212,600 on butane | 1,285,200 printed |
| bowen-mountain | 8 MR-750s, two a flue (Fig 4-153) | propane, 11 in. w.c. (assumed, p.215, p.227) | 72,000 (Ward's low-pressure orifice) | 576,000 |
| W16 (p.227–228) | 4 simple air mixers, #34 | natural gas, 8 in. w.c. (printed) | 45,380 (orifice equation); 50,000 printed; Rule 4's 45 ft³/hr | 181,500; 200,000 printed |
| olsen-crossdraft-36 | 6 at 36,000 (p.226) | natural gas, 8 in. w.c. (assumed) | 36,000 (the rating) | 216,000 |
| W15 (p.226) | 10 "such burners" | the same | 36,000 | 360,000 |
| olsen-kit-16 | 8 MR-750s (assumed: the inlet's count) | natural gas, 8 in. w.c. | 75,000 | 600,000 |
| kaneko-car | 32 MR-100s (assumed) | natural gas, 8 in. w.c. | 100,000 | 3,200,000 |
| updraft-test-1 to 4 | 12, 12, 14, 18 MR-750s (assumed) | natural gas, 8 in. w.c. | 75,000 | 900,000–1,350,000 |
| kahler-salt, blakebrough-tasmania | 4 power burners; 4 compound injectors | not printed | not sourced | refused |

W16's printed 50,000 a burner is about 10 % over what its own #34 at 8 in. gives by the equation
(Ward's basis) and by Rule 4's 45 ft³/hr: the book's sizing and its orifice disagree by that much.

## 4. What a firing needs against what the burners give (Derived, v2)

`target.input_for` on each kiln's model (its setting's band, λ 1.0–1.15: the operator's, no
draft path yet):

| Kiln | Printed | Burners give | v2: the input for the printed time | v2: the time on the burners |
|---|---|---|---|---|
| olsen-kit-24 | 8 h (p.139) | 750,000 | 220,000–378,000 for 8 h (the band's corners) | 0.97–3.51 h |
| W15 | about 8 h (p.226) | 360,000 | 198,000–322,000 for 8 h (0.55–0.89 ×) | 2.6–6.8 h |
| olsen-crossdraft-36 | 12–15 h (p.226) | 216,000 | 368,000–417,000 for 15 h, 438,000–502,000 for 12 h (λ 1) | 34–39 h at λ 1; not in 48 h at λ 1.15 |

The kits and W15 are overpowered by Olsen's own word (p.226): their burners give two to three times
what their printed firings need. The cross-draft is the open item it was (§I), now on its setting's
own band: 1.7–2.3 × the six burners' rating.

## 5. The kits' burner spacing (B4–B6 step 7's question)

With their counts kept (from their inlets), the kits' burners fall 15.2 in (the 16), 19.6 in (the
24's eight round the edge), 13.0 in (the 50) and 12.0 in (the 100) apart round the floor, against
Olsen's 9–12 in (p.171). By the charts, the 16's eight MR-750s give 600,000 BTU/hr at 8 in. w.c. on
natural gas and the 24's ten 750,000: both reach cone 10 in 1–3.5 h across their bands, well inside
the 24's printed eight hours. Spaced 9–12 in, the same perimeters would take 10–14 burners round the
16's floor and 13–17 round the 24's (Derived from the spacings above: 8 × 15.2 in and 8 × 19.6 in),
more heat still, where the inlet's count already gives two to three times what the firing needs.
The spacing stays the owner's question (B4–B6); the kits aren't resized.
