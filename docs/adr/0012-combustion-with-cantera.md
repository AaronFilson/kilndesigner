# 12. Combustion is modelled with Cantera, not a rule of thumb

- **Status:** proposed
- **Date:** 2026-10-21

## Context

Whether a hybrid kiln should run its elements or its burners at a given temperature depends on
what a unit of heat *kept in the kiln* costs. For gas that depends on how much heat leaves with
the flue gas, which grows steeply with the kiln's temperature and changes with excess air and
reduction. No published kiln source gives this as a table, and a fixed "gas kilns are 30%
efficient" figure would be wrong at most temperatures.

## Decision

- Use Cantera with the GRI-Mech 3.0 mechanism to compute the *available heat*: the enthalpy of
  the reactants at the air temperature minus that of the equilibrium products at the flue
  temperature, per kg of propane, as a fraction of the published higher heating value.
- Assume the flue gas leaves at the kiln's temperature (no recuperation), oxidising firing at 3%
  dry flue oxygen, and reduction at λ = 0.9.
- Check it in CI against published figures: the adiabatic flame temperature in air (3,595 °F)
  and the lower heating value (46.6 MJ/kg).

## Consequences

- The cost curves and the switch-over come from thermodynamics, with sources, rather than a
  guess, and they move correctly with prices, excess air and reduction.
- Cantera is a 5 MB dependency of the engine; it's imported only when gas is analysed.
- Cost per firing still needs the firing schedule and the stored heat (M6).

## In an interview

"The question 'when should a hybrid kiln switch from elements to gas' comes down to available
heat, so I computed it from first principles with Cantera and checked it against published
flame temperatures. It showed that at Pacific Northwest prices electricity is cheaper at every
temperature, which turned the design question from cost to element life."
