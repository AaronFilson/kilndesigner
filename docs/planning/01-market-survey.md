# 01 - Market survey

Status: draft. Research checked on 2026-10-21. Prices and claims are as found on that date unless a different date is given.

## Purpose

kilndesigner will take a kiln spec and produce:

- parametric 3D geometry
- heat-loss and firing simulation
- electric element design (Kanthal-type wire sizing)
- gas burner and flue sizing
- wood-kiln proportions
- printable plans and a bill of materials (brick counts, cut lists)

It will run as a hosted app with accounts and as a self-hosted or local tool.

This survey asks what already exists and what is missing. It covers ceramics first, then glass, wood, gas, electric, raku, and enameling or metal-clay kilns.

## Short answer

Nobody sells kiln design software for potters. Today people design kilns with:

1. books (mainly Olsen's *The Kiln Book*),
2. vendor charts and PDFs (Kanthal, Ward Burner),
3. forum threads, and
4. their own spreadsheets.

Good tools exist in pieces, and each piece lives somewhere else. Refractory makers have solid heat-flow calculators, but they are built for industrial linings. They do not do elements, burners, geometry, or plans. Nothing joins these steps into one tool. That is the opening.

## How to read this

Each entry says what the thing does, what it costs, who uses it, how good it is, and what is missing. "Not verified" means I could not confirm it from a primary source.

---

## 1. Element and burner calculators

### Kanthal design guides (element wire)

- **What it does:** Free PDFs and web pages that explain how to size resistance wire. The method is to find wire diameter and length first, then coil diameter and pitch. Wire size depends on surface load and alloy. Kanthal also publishes resistivity tables and a temperature factor. [Kanthal design calculations](https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/appendixexplanations2/design-calculations-for-heating-elements/), [wire element PDF](https://prodshop.kanthal.com/contentassets/3720091e7e604cf89d4a289536f6b56b/design-calculations-of-wire-elements.pdf)
- **Price:** Free.
- **Who:** Engineers, element winders, and DIY kiln builders.
- **How good:** This is the authoritative method and data. Most other element advice traces back to it.
- **Missing:** I found no interactive Kanthal calculator, only documents and tables. Users must do the math by hand or in a spreadsheet. Nothing ties it to kiln geometry or groove layout.

### Euclid's, Duralite, and other element vendors

- **What they do:** They sell wire and wound elements and will design or wind elements to order. Duralite has quote and replacement-request forms and a wire spec page. [Euclid's](https://www.euclids.com), [Duralite](https://www.duralite.com), [Duralite wire specs](https://duralite.com/resistance-wire-specifications/)
- **Price:** The design help is free with a purchase. Elements are priced per order.
- **Who:** Kiln owners who are replacing elements, and small builders.
- **How good:** Reliable for replacement parts. It is a human service, not a tool.
- **Missing:** No public calculator from Euclid's or Duralite (I checked their sites). I could not find a Duralite calculator at all.

### Sentro Tech

- I found no element calculator or kiln design tool from Sentro Tech. It makes lab furnaces and production kilns. [Directory listing](https://mrforum.com/materials-research-equipment-directory/1822/sentro-tech-strongsville-oh-usa)

### MHI GAXP heating element worksheet

- **What it does:** A six-step worksheet for sizing one maker's elements in a new furnace. It goes from chamber size and temperature to power, adds about 50% for poor insulation or fast heat-up, then gives element length and the parts count. It links to separate furnace-power and coil-power calculators. [MHI worksheet](https://mhi-inc.com/PG3/GAXPMaterial.htm)
- **Price:** Free.
- **How good:** A good model of the "power, then elements, then parts list" flow.
- **Missing:** It covers MHI products only and lab furnaces, not pottery kilns.

### "Heating Element Calculator" iOS app

- **What it does:** Calculates wattage, coil design, and amperage for a given temperature and element size. Made by Caladan Software. Last updated May 2023. [App Store](https://apps.apple.com/us/app/id1227516847)
- **Price:** $999.99 (checked 2026-10-21).
- **How good:** I did not test it. The price suggests it is aimed at industry.
- **Missing:** iOS only. No geometry, heat loss, or plans.

### Ward Burner Systems data guide (gas burners)

- **What it does:** Ward sells burners, valves, and orifices. Its free data guide gives BTU per cubic foot per hour by wall type and cone. For example, 9 in. insulating brick at cone 10 needs 10,000 to 16,000 Btu/cf/hr, and 6 in. fiber at cone 10 needs 7,000 to 10,000. Multiply by kiln volume, then divide by the number of burners. The high end of each range gives about a 6 to 7 hour firing. It also has separate raku figures and orifice charts. [Ward data guide](https://wardburner.com/technical-info/data-guide/), [Ward Burner](https://wardburner.com)
- **Price:** The guide is free. Burners are sold separately.
- **Who:** Gas and raku kiln builders. Forum posters often point new builders here. [Ceramic Arts Daily thread](https://community.ceramicartsdaily.org/topic/20073-one-burner-10-cubic-ft-gas-kiln/)
- **How good:** Simple and widely trusted for rough sizing.
- **Missing:** It is a lookup table. It does not cover flue or chimney sizing, it does not model heat loss, and it does not handle burner placement.

### Digitalfire / Clachrie burner book

- **What it does:** Tony Hansen's Digitalfire is converting J. R. (Jim) Clachrie's 1970s gas kiln and burner design book to the web. It covers combustion, safety, burner design, refractories, and downdraft kiln proportions, with an 18 cu ft example. The page is marked "under construction." [Digitalfire burner book](https://digitalfire.com/burnerbook/index.php)
- **Price:** Not stated. It appears free to read on the web.
- **How good:** It is written by a gas burner engineer. Some of the content is old.
- **Missing:** Text only. No calculator.

### Brick and arch calculators

- I found no kiln-specific brick or arch calculator. People use general catenary math. One blog post works through a real kiln arch, 41 by 39.5 in., to estimate end-wall bricks. [John D. Cook, "Catenary kiln"](https://www.johndcook.com/blog/2022/03/01/catenary-kiln/), [Rechneronline catenary calculator](https://rechneronline.de/pi/catenary-arc.php)
- **Missing:** No tool turns an arch shape into arch-brick counts, skewback angles, or cut lists.

---

## 2. Refractory and insulation heat-loss tools (best in class)

These come from industrial insulation and refractory makers. They show what a mature heat-loss tool looks like.

### Morgan Thermal Ceramics "Heat Flow"

- **What it does:** A web-based steady-state heat-flow calculator using ASTM C680. At launch it came with about 400 Morgan products (Superwool, Kaowool, firebrick, castables) and let users add their own materials. Users could save calculations and export PDFs. There were mobile apps. [Chemical Processing, 2014](https://www.chemicalprocessing.com/vendor-news/2014/morgan-releases-heat-flow-calculator), [World Pipelines, 2014](https://www.worldpipelines.com/product-news/21102014/Morgan-release-Heat-Flow)
- **Price:** Free with registration (as of launch).
- **Status:** morganheatflow.com loads with a title only. I could not confirm that it still works (checked 2026-10-21).
- **Missing:** Steady state only. It gives no heat-up time, no stored heat per firing, no geometry, and nothing on elements or burners.

### Alkegen (Unifrax) Heat Flow Program v4.0

- **What it does:** A downloadable program, requested through a form. It estimates cold-face temperature, heat loss, and heat storage for refractory and insulation linings. It also compares lining designs for fuel savings and CO2. [Alkegen Heat Flow Program](https://www.alkegen.com/?p=16067) (the page returned 403 when fetched; details are from the search snippet)
- **Price:** Free on request (not verified).
- **How good:** Includes heat storage, which matters for intermittent kilns.
- **Missing:** Desktop only. Covers only its own products. Industrial focus.

### HarbisonWalker International (HWI, now part of Calderys) Heat Transfer tool

- **What it does:** A web tool for heat transfer through refractory linings. It was updated in 2018 to the newer ASTM C680 method, which tends to give higher shell temperatures. [HWI update](https://thinkhwi.com/heat-transfer-tool-updated/)
- **Price:** Not stated.
- **Missing:** The page does not say whether it handles transient heating.

### NAIMA 3E Plus

- **What it does:** Insulation thickness and heat-loss software from the North American Insulation Manufacturers Association. Based on ASTM C680. It covers energy, cost, and emissions, and builds thickness tables. It is moving to a web tool at 3EPlus.org. [Insulation Institute](https://insulationinstitute.org/tools-resources/free-3e-plus)
- **Price:** Historically free. I could not confirm the terms of the web version.
- **Missing:** Built for pipes and equipment at moderate temperatures, not kiln hot faces.

### Calderys and RHI Magnesita engineering services

- **What they do:** Both offer lining design as an engineering service, not as software. RHI Magnesita lists multi-dimensional heat-flux calculations, stress analysis, and CAD-based refractory engineering. Calderys does custom design including heat-transfer calculations and drawings. [RHI Magnesita](https://www.rhimagnesita.com/industries-we-serve/environment-energy-chemistry/), [Calderys copper foundries brochure](https://calderys.com/Calderys-Meet-2024/assets/Copper_foundries_CALDERYS.pdf)
- **Price:** Quoted per project.
- **Takeaway:** "Best in class" here is: a product library with real data, ASTM C680 math, multi-layer walls, cold-face temperature, heat storage, fuel cost and CO2, and drawings. None of it is sized or priced for a studio potter.

---

## 3. General CAD, FEM, and thermal tools

People do use general engineering tools for kilns. Each one needs skill and covers only one step.

| Tool | What it does for kilns | Price (checked 2026-10-21) | Missing |
|---|---|---|---|
| [Autodesk Fusion](https://www.autodesk.com/products/fusion-360/blog/fusion-subscription-types/) | 3D CAD. Its Simulation Extension adds thermal simulation. | About $680/yr base ([third-party guide, Aug 2026](https://vagon.io/blog/fusion-360-pricing)). Extensions are $595 to $1,465 per year each (Autodesk). | No kiln materials or rules. You have to model everything yourself. |
| SolidWorks + Simulation | CAD with thermal FEA. | Commercial license. I did not verify the price. | Same as Fusion. Expensive for hobbyists. |
| Ansys / COMSOL | Full CFD and FEM. Published studies use Ansys CFX to model catenary kilns for Brazilian potters. [Cerâmica 2022](https://doaj.org/article/d191f9290d974273bdc15032feec6c06) | Commercial. Price on request. | Research-grade. Weeks of setup. Out of reach for potters. |
| [FreeCAD FEM + CalculiX](https://wiki.freecad.org/FEM_SolverCalculixCcxtools) | Free CAD with steady and transient heat transfer. | Free, open source. | Hard to learn. The transient tutorial is unfinished. No kiln templates. |
| [Energy2D](https://concord.org/blog/energy2d-now-available/) | Free 2D simulator for conduction, convection, and radiation. Good for teaching. | Free, open source. | 2D only. I found no kiln models for it. |
| OpenSCAD | Parametric CAD in code. RepKiln uses it for brick layouts (see section 7). | Free. | Geometry only. |
| Spreadsheets | The real everyday tool. Builders keep coil, BTU, and brick spreadsheets. | Free. | Error-prone. Every builder starts over. Nothing is shared. |

---

## 4. Kiln makers: do they have design or configure tools?

Short answer: they have product filters, spec sheets, and "call us" custom work. None has a design tool.

| Maker | Online tool | Custom work | Source |
|---|---|---|---|
| Skutt | "Build A Spec" tool prints a spec page for a chosen model. Parts Finder. KilnLink cloud monitoring. | Not stated. | [Skutt specs](https://skutt.com/?p=13571), [KilnLink](https://skutt.com/?p=94) |
| L&L | "Find Your Kiln" filter by volts, phase, loading, shape, height, capacity, and cone. Shows list prices. | Through sales. | [L&L Find Your Kiln](https://hotkilns.com/choose-your-kiln) |
| Paragon | "How to Choose a Kiln" guide, "Ask The Kiln Guru," element search. Site calls itself "Home of Custom Kilns." | Yes, by contact. | [Paragon](https://paragonkilns.com/) |
| Olympic | No configurator found. Gas models come with fuel and option choices. | "Custom kilns quoted upon request." | [NM Clay listing](https://nmclay.com/kilns/olympic-kilns), [The Ceramic Shop](https://www.theceramicshop.com/product/7049/olympic-torchbearer-18/) |
| Bailey | No configurator found. Buyers are told to call. Has built custom gas kilns. | Yes. | [Ceramic Arts Daily thread](https://community.ceramicartsdaily.org/topic/5935-buying-a-gas-kiln/), [Worcester Craft Center list](https://worcestercraftcenter.org/wp-content/uploads/2023/01/Ceramics-Studio-Equipment.pdf) |
| Geil | No configurator found. The site did not resolve when I checked. One forum report says Geil does not design kilns for the end user (secondhand). | Unclear. | [Ceramic Arts Daily thread](https://community.ceramicartsdaily.org/topic/23454-geil-medium-duty-gas-kiln/) |
| Blaauw | No configurator found. Builds custom, computer-controlled gas kilns for schools. One 144 cu ft kiln was reported at $200,000. | Yes. | [UW report](https://depts.washington.edu/soanews/online/2011/04/21/mr-peeper-is-here), [Pewabic](https://www.pewabic.org/products/donation-kiln-project-campaign) |
| Nabertherm | No configurator found. Offers "individual project planning" and tailor-made systems. | Yes. | [Nabertherm](https://www.nabertherm.com) |
| Rohde | No configurator found. Standard catalog ranges. | Not stated. | [Rohde](https://www.rohde.eu/en/arts-and-crafts/company/news/seminar-and-30th-anniversary-at-rohde-partner-mtl-brock) |

**Takeaway:** Makers help you pick a kiln they already make. Nothing helps you design one.

---

## 5. Books and plan sets (the real "software" today)

| Book | What it gives | Notes |
|---|---|---|
| Frederick L. Olsen, *The Kiln Book* | Design, refractories, bricklaying, arches, flues, burners, electric elements, safety. Plans for crossdraft, downdraft, updraft, and electric kilns, including the Fastfire wood kiln. First published 1973. | 4th ed. 2011 (A&C Black / Penn Press). A new edition from Dorrance came out in 2023, listed at $96 paperback, 318 pp. [Penn Press](https://pennpress.org/?p=849), [listing](https://www.gandhi.com.mx/the-kiln-book-9798887299525/p) |
| Daniel Rhodes, *Kilns: Design, Construction, and Operation* | History, materials, and design principles. | Chilton, 1968; 2nd ed. 1981. Out of print. Readers call it "a little dated." [Library record](https://libcat.library.tamu.edu/Record/in00000629656), [Alibris](https://origin-www.alibris.com/Kilns-Design-Construction-and-Operation-Daniel-Rhodes/book/3549407?qcond=6) |
| Coll Minogue and Robert Sanderson, *Wood-fired Ceramics: Contemporary Practices* | Wood kiln types, firing logs, and kiln plans from 60+ artists. | 2000. [The Log Book story](https://thelogbook.net/story.html), [UW library](https://search.library.wisc.edu/catalog/999887800602121) |
| Joe Finch, *Kiln Construction: A Brick by Brick Approach* | Three tested kilns (gas, oil, wood), with step-by-step builds. | 112 pp. New Penn Press edition 2024. [Penn Press](https://www.pennpress.org/9781512827224/kiln-construction) |
| Steve Harrison, *Laid Back Wood Firing* | Wood kiln plans that show the main variations. | 8th ed. 2023. [Australian Ceramics](https://australianceramics.com/shop/laid-back-wood-firing-by-steve-harrison-tg1) |
| Ian Gregory, *Kiln Building* | Kiln types, fuels, materials, and principles. | 2002, Ceramics Handbooks series. [eBay listing](https://www.ebay.co.uk/p/91728297) |

I found no single well-known "brickmaking plans" product. The Bourry box design spreads mostly through books and personal plans, such as Ray Finch's plans described in *Studio Potter*. [Studio Potter](https://www.studiopotter.org/node/429)

**How good:** Olsen is the standard reference. The books are trusted and full of rules of thumb.

**Missing:** Static plans at fixed sizes. If you change the size, you redo the math by hand. US and metric units get mixed. Nothing checks your numbers.

---

## 6. Communities and plan sources

| Source | What it offers | Missing |
|---|---|---|
| [Ceramic Arts Daily forum](https://community.ceramicartsdaily.org/topic/22034-kiln-build-from-scratch/) | The busiest English kiln-build forum. Threads on element winding, burners, and DIY builds. | Advice is scattered and sometimes contradictory. No tools. |
| [Ceramic Arts Network articles](https://ceramicartsnetwork.org/daily/article/the-sasukenei-smokeless-kiln-a-wood-kiln-that-produces-little-smoke-and-great-results/) | Feature articles on specific kilns. | Articles, not plans you can resize. I did not find a kiln-building ebook. |
| [Digitalfire (Tony Hansen)](https://digitalfire.com/glossary/kiln+controller) | Deep pages on controllers, firing schedules, and kiln monitoring. Insight-Live is a glaze and recipe tool. | Firing-focused. Kiln construction is mostly the burner book project. |
| [Glazy](https://www.derekau.net/blog/2016/01/10/glazy-open-source-ceramics-recipes-library) | Open-source glaze database (Laravel). | No kilns. It is a useful model for an open, community-run ceramics app. |
| [The Log Book](https://thelogbook.net/) | Wood-firing journal. About 400 articles. | Stopped publishing in Dec 2020. Archive only. |
| Reddit r/Pottery | General pottery community. | I did not verify specific kiln-design threads there. |
| [WarmGlass forum](https://www.warmglass.com/phpBB3/viewtopic.php?p=339543) | Glass kiln plans and DIY threads. | Same issues as other forums. |
| [Ganoksin Orchid](https://orchid.ganoksin.com/t/building-a-kiln/9286), [SNAG tech article](https://snagmetalsmith.org/wp-content/uploads/2024/09/TechArticle_Jan_2013.pdf) | Enameling and metal-clay kiln DIY notes, including torch-fired fiber cans. | No tested plans for metal clay. |
| [Instructables top-loader](https://instructables.com/Electric-Kiln-Top-Loader) | A 120 V soft-brick kiln for PMC and enameling, under $70 without the controller. | One fixed design. Safety is up to the builder. |

---

## 7. Glass, raku, and small-kiln DIY

- **Glass fusing:** Forum advice favors fiber linings for fast heating and cooling, and top elements for fusing. One hobby build used 1 in. fiber rated to 2300 F with mullite tubes holding Kanthal coils. Commercial examples include the Paragon FiberFuse. [WarmGlass](https://www.warmglass.com/phpBB3/viewtopic.php?p=339543), [Hackaday glass kiln](https://hackaday.io/project/2979)
- **Raku:** Most DIY raku kilns are trash cans or wire cages lined with fiber. The Bracker kit uses 1/2 in. rigidized blanket. [Pottery Wheel guide](https://thepotterywheel.com/how-to-make-a-raku-kiln/), [Bracker kit](https://www.clay-king.com/product/brackers-raku-kiln-kit/)
- **Missing:** No tool sizes the burner port and flue for a raku can, or plans element layout for a glass kiln with a large flat floor.

---

## 8. Kiln controllers (adjacent)

These run firings. They do not design kilns. They matter because they produce real firing data that could check a simulation.

| Product | What it does | Price / model | Source |
|---|---|---|---|
| Bartlett Genesis | Touchscreen controller used by L&L and others. Graphs, stored programs, diagnostics, Wi-Fi. | Sold with kilns or as an upgrade. | [The Ceramic Shop](https://www.theceramicshop.com/product/26586/genesis-mini-control-board/), [Ceramic Industry](https://www.ceramicindustry.com/articles/95468-ll-kilns-optional-genesis-touchscreen-control) |
| Skutt KilnLink | Cloud monitoring. Firing history, amps per section, voltage. Text alerts. | Free status app. Premium is $100/yr for history (retailer listing). | [Skutt](https://skutt.com/?p=94), [The Ceramic Shop](https://www.theceramicshop.com/product/11670/kiln-link-premium-1-yr-plan/) |
| Orton AutoFire | Standalone controller. Can drive a kiln vent. | Sold in packages. | [Ceramic Arts Daily thread](https://community.ceramicartsdaily.org/topic/38928-help-comparing-standalone-controllers-orton-autofire4000-vs-olympic-electro-sitter-w-genesis/) |
| TAP Kiln Control (SDS Industries) | Controller with a remote-control mobile app and schedule sync. | Free tier plus premium. | [TAP help page](https://help.kilncontrol.com/knowledge/how-does-tap-kiln-control-mobile-app-compare-to-kiln-control-apps-from-manufacturers-like-bartlett-orton-and-skutt) |
| [jbruce12000/kiln-controller](https://github.com/jbruce12000/kiln-controller) | Open-source Raspberry Pi controller. Python, GPL-3. 301 stars. Schedules, PID, cost estimates, and a simulation mode. | Free. | GitHub, checked 2026-10-21 |
| [Saur0o0n/PIDKiln](https://github.com/Saur0o0n/PIDKiln) | ESP32 PID kiln controller. 174 stars. | Free. | GitHub |
| [RinthLabs/PyKiln](https://github.com/RinthLabs/PyKiln) | Web-based kiln controller in Python. Inactive since 2021. | Free. | GitHub |

Digitalfire warns that DIY controllers lack UL or CSA listing and may not handle stuck relays. [Digitalfire](https://digitalfire.com/glossary/kiln+controller)

---

## 9. Open source on GitHub

I searched GitHub for kiln design, heat loss, element, Kanthal, and refractory terms. I found almost nothing for kiln design itself (checked 2026-10-21).

| Repo | What it is | Notes |
|---|---|---|
| [mattmoses/RepKiln](https://github.com/mattmoses/RepKiln) | A small DIY kiln with OpenSCAD brick layouts, coil and heat-transfer spreadsheets, and Python scripts (`kiln_heatup.py`, `kiln_model_matching.py`). These solve the 1D transient heat equation and fit it to measured data. [Hackaday](https://hackaday.io/project/21642) | The closest thing to kilndesigner, at a tiny scale. 8 stars. No license file. One fixed kiln. |
| [CalebBell/ht](https://github.com/CalebBell/ht) | A general Python heat-transfer library, MIT. Covers insulated objects and radiation. | Not kiln-specific. A possible dependency. |
| [MehrzadKhademi/furnace-wall-temperature-profile](https://github.com/MehrzadKhademi/furnace-wall-temperature-profile) | 1D steady-state furnace wall model in Python. | 0 stars. A student-scale project. |
| Controllers | See section 8. | Firing, not design. |

Many repos named "kiln" are unrelated software projects (AI tools, build tools).

---

## Gap analysis

### What no single product does

1. **Join the steps.** Today the steps are: pick a size, choose a wall, check heat loss, size the elements or burners, size the flue, draw it, and count bricks. Each step uses a different source. Nothing carries one spec through all of them.
2. **Resize a plan.** Books give fixed plans. Change the chamber by 6 in. and you redo every number by hand.
3. **Transient firing for studio kilns.** The industrial tools are steady state. For a kiln that fires once a week, the questions are "how long to cone 10" and "how much fuel or kWh per firing." Answering that needs heat storage in the walls. Only Alkegen mentions heat storage, and only for industrial linings.
4. **Element design tied to geometry.** Kanthal gives the math. No tool turns "this chamber, this voltage, this breaker" into wire gauge, coil size, groove layout, and surface-load checks.
5. **Gas and flue sizing in one place.** Ward gives BTU tables. Flue and chimney sizing is still rules of thumb in books.
6. **Wood-kiln proportions.** Firebox, grate, throat, chamber, and chimney ratios live only in books (Olsen, Harrison, Minogue and Sanderson).
7. **Plans and a bill of materials.** No tool outputs printable drawings, brick counts by shape (straights, arches, wedges, skewbacks), cut lists, or a materials budget.
8. **Open and local.** The serious tools are vendor-locked (one maker's products), desktop-only, or closed. No open, self-hostable kiln design tool exists.
9. **Feedback from real firings.** Controllers log real temperature curves. Nothing compares those curves to the design model. RepKiln did this once, by hand.

### Where kilndesigner can stand out

- **One spec in, a full package out.** Geometry, heat loss, elements or burners, flue, drawings, and BOM, all from one file. This is the core difference.
- **Parametric books.** Encode the well-known rules (Olsen-style proportions, Ward BTU ranges, Kanthal surface loads) as checked, cited defaults. Users can resize and see what changed.
- **Transient firing estimate.** A 1D multi-layer model with heat storage gives time to temperature and energy per firing. Start simple, and say clearly that it is an estimate.
- **Open material library.** IFB, hard brick, fiber, castables, and wire alloys, with sources. Vendor-neutral, unlike Morgan, Alkegen, or HWI.
- **Brick-level output.** Course-by-course layouts, arch brick counts, and cut lists. No one does this.
- **Local and hosted.** A Python core that runs offline, plus a hosted version for accounts and sharing. Glazy shows that an open ceramics app can build a community.
- **Controller import later.** Read logs from kiln-controller, Genesis, or KilnLink exports to tune the model against real firings.
- **Safety in plain view.** Warn when surface load, amps, breaker size, or clearances are out of range. Do not present the output as a substitute for a qualified electrician, a gas code inspection, or a listed controller.

### Risks and notes

- **Liability.** Electric and gas design touches code and safety. Output must carry warnings, and should recommend listed parts and a professional review.
- **Data quality.** Material properties vary by maker and temperature. Cite every value and let users override it.
- **Small market.** DIY kiln builders are a niche. Schools, community studios, and small makers who build gas and wood kilns are the likely paying users. Hobby electric builders will mostly use the free local version.
- **Unverified items.** Morgan Heat Flow's current status, the Alkegen price, the HWI price, and specific Reddit threads were not verified. Recheck these before relying on them.
