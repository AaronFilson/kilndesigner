"""Engine v2's heat model: the firing as gas zones, walls, the setting and the gas path in time.

Built from the tools the thermal survey adopted (`docs/research/thermal-software.md`,
`thermal-combinations.md`; the user, 2026-11-10): Cantera for the gas (equilibrium products,
enthalpy, transport), fluids for the draft, trimesh + embreex for radiation between faces with
the setting in the way, a published weighted-sum-of-grey-gases set for gas radiation, SUNDIALS IDA
(scikit-sundae) for the firing as a DAE, scikit-fem for the ground.

The reference kilns all worked for their builders (the user, 2026-11-10): where v2 says one can't
reach its documented firing on its own burners or fuel and its own draft, the model or the design
file's inputs are at fault, and the missing physics or input is named. Nothing is fitted to a kiln
(ADR 0017, decision 4); a quantity no source gives is a stated band or a stated test input.
"""
