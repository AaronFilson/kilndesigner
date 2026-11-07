# Natural gas prices (US), for reference only

Informational. The engine has **no default** natural gas price: `site.natural_gas_price` is the
user's own rate from their bill (for example `1.5822 USD/therm`). Left out, the firing's cost
isn't given. These figures show the range a rate is likely to fall in; nothing reads them.

Source: U.S. Energy Information Administration (EIA), Natural Gas Prices, release date
2026-10-30, read 2026-11-06. Prices are delivered prices in dollars per thousand cubic feet
($/Mcf), taxes and delivery included as EIA reports them.

## National average, monthly

<https://www.eia.gov/dnav/ng/ng_pri_sum_dcu_nus_m.htm>

| Month | Residential ($/Mcf) | Commercial ($/Mcf) |
|---|---|---|
| Mar 2026 | 16.16 | 12.26 |
| Apr 2026 | 18.04 | 12.21 |
| May 2026 | 19.73 | 12.17 |
| Jun 2026 | 24.09 | 12.71 |
| Jul 2026 | 26.45 | 13.03 |
| Aug 2026 (latest) | 27.05 | 12.87 |

Residential prices are highest in summer, when little gas is sold over the same fixed charges.

## Annual 2025, national and by state

- Residential: <https://www.eia.gov/dnav/ng/ng_pri_sum_a_EPG0_PRS_DMcf_a.htm>. US $15.34/Mcf;
  lowest Idaho $7.69, highest Hawaii $52.38.
- Commercial: <https://www.eia.gov/dnav/ng/ng_pri_sum_a_EPG0_PCS_DMcf_a.htm>. US $10.98/Mcf;
  lowest New Mexico $6.34, highest Hawaii $39.04 (some states, among them Maine, Maryland and
  New Jersey, show no 2025 figure).

## Per therm

A therm is 100,000 BTU. At the 1000 BTU/ft³ that Olsen's orifice tables take (The Kiln Book,
4th ed., p.230; `gas.yaml`), 1 Mcf is 10 therms, so $15.34/Mcf is about $1.53/therm. The real
heat content of pipeline gas varies and is printed on the bill; a rate per therm avoids it.

Not found: an EIA national average stated directly per therm.
