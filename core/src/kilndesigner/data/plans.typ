// Kilndesigner plans. The data comes from data.json, written by kilndesigner.plans.
#let d = json("data.json")

#set document(title: d.name, author: "Kilndesigner", date: none)
#set page(
  paper: d.paper,
  margin: (x: 1.8cm, y: 2cm),
  numbering: "1 of 1",
  header: context {
    if counter(page).get().first() > 1 [
      #set text(size: 8pt, fill: luma(110))
      #d.name #h(1fr) Kilndesigner #d.engine_version
    ]
  },
)
#set text(size: 9.5pt, lang: "en")
#set par(justify: false, leading: 0.6em)
#set heading(numbering: "1.")
#show heading.where(level: 1): it => { v(0.4em); it; v(0.2em) }
#set table(stroke: 0.4pt + luma(170), inset: 4pt)
#show table.cell.where(y: 0): set text(weight: "bold")

#let level-colour(level) = if level == "error" { rgb("#b3261e") } else if level == "warning" { rgb("#a15c00") } else { luma(90) }

#align(center)[
  #text(size: 20pt, weight: "bold")[#d.name]
  #v(0.2em)
  #text(size: 11pt)[Kiln plans and working · Kilndesigner #d.engine_version]
]
#v(0.6em)

#block(fill: rgb("#fff4e5"), inset: 8pt, radius: 3pt, width: 100%)[
  *Safety.* These plans are engineering guidance from the design file, not an approved design.
  Electrical work must meet your local code and be checked by a licensed electrician; gas work
  by a licensed gas fitter. Every number below shows its working and source so it can be checked.
]

= Summary
#table(
  columns: (auto, 1fr),
  [Item], [Value],
  ..d.summary.map(row => (row.at(0), row.at(1))).flatten()
)

= Findings
#for f in d.findings [
  - #text(fill: level-colour(f.level), weight: "bold")[#upper(f.level)] #f.message
    #if f.reference != none [ #text(size: 8pt, fill: luma(110))[(#f.reference)] ]
]

= Lining
#table(
  columns: (auto, 1fr, auto, auto, auto),
  [Face], [Layers, hot face first], [Hot side], [Outside], [Heat loss],
  ..d.faces.map(f => (
    f.face,
    f.layers.map(l => l.material + " " + l.thickness).join(", "),
    f.layers.first().hot_side,
    f.surface_temperature,
    f.heat_loss,
  )).flatten()
)

= Drawings
#for v in d.views [
  #figure(image(v.file, height: 9.5cm), caption: v.title)
]

#if d.elements != none [
  = Elements
  #table(
    columns: (auto, 1fr),
    [Item], [Value],
    ..d.elements.map(row => (row.at(0), row.at(1))).flatten()
  )
]

#if d.gas != none [
  = Burners, propane and chimney
  #table(
    columns: (auto, 1fr),
    [Item], [Value],
    ..d.gas.rows.map(row => (row.at(0), row.at(1))).flatten()
  )
  == Propane supply at #d.gas.supply_temperature
  #table(
    columns: (1fr, auto, auto),
    [Supply], [Capacity], [Meets the design input?],
    ..d.gas.supply.map(s => (s.case, s.capacity, if s.meets_demand [yes] else [*no*])).flatten()
  )
  == Other burner choices
  #table(
    columns: (1fr, auto, auto, auto, auto),
    [Burner], [Count], [Pressure], [Each], [Cost],
    ..d.gas.options.map(o => (o.model, str(o.count), o.pressure, o.each, "$" + str(calc.round(o.total_cost, digits: 2)))).flatten()
  )
]

= #d.frame.title
#if d.frame.thrust != none [Design thrust of the arch: #d.frame.thrust.]
#table(
  columns: (1fr, auto, auto, auto),
  [Part], [Steel], [Count], [Length each],
  ..d.frame.rows.flatten()
)

#if d.castables.len() > 0 [
  = Castables you mix
  #for c in d.castables [
    == #c.name
    #table(
      columns: (1fr, auto, auto),
      [One batch], [Weight], [Share],
      ..c.batch.flatten()
    )
    #table(
      columns: (auto, 1fr),
      [Item], [Value],
      ..c.rows.flatten()
    )
    #for s in c.steps [+ #s
    ]
    #if c.schedule.len() > 0 [
      #table(
        columns: (auto, auto, auto, 1fr),
        [First firing to], [Rate], [Hold], [Why],
        ..c.schedule.flatten()
      )
    ]
    #for l in c.layers [- #l
    ]
  ]
]

#if d.hybrid != none [
  = Elements and burners together
  #table(
    columns: (auto, 1fr),
    [Item], [Value],
    ..d.hybrid.rows.map(row => (row.at(0), row.at(1))).flatten()
  )
  #for c in d.hybrid.at("charts", default: ()) [
    #image(c, width: 100%)
  ]
  The first chart is what each kWh that stays in the kiln costs: an element keeps all of its
  energy in the kiln, but a burner loses what goes up the chimney, which grows with the kiln's
  temperature. The second is the element power left over after the kiln's steady heat loss: what
  is left to heat the ware and walls.
]

#if d.course_plans.len() > 0 [
  = Brick course plans
  Each drawing shows one layer as seen from inside the kiln, course by course from the bottom
  (walls) or from the front (floor and roof). Whole bricks are pale; cut pieces are orange.
  Odd and even courses start differently so that the joints don't line up.
  #for c in d.course_plans [
    #block(breakable: false)[
      == #c.title
      #c.description
      #image(c.file, height: 7.5cm)
    ]
  ]
]

= Cut list
#if d.cut_list.len() == 0 [No cuts.] else [
  #table(
    columns: (auto, 1fr, auto),
    [Material], [Cut], [Pieces],
    ..d.cut_list.map(c => (c.material, c.cut, str(c.count))).flatten()
  )
]

= Bill of materials
#table(
  columns: (1fr, auto, auto, auto),
  [Item], [Buy], [Price each], [Cost],
  ..d.bom.lines.map(l => (
    [#l.item \ #text(size: 8pt, fill: luma(100))[#l.needed]],
    l.buy,
    if l.unit_price == none [—] else [#l.unit_price],
    if l.cost == none [—] else [#l.cost_text],
  )).flatten(),
  table.cell(colspan: 3)[*Total, priced items*], [*#d.bom.total_text*],
)
#text(size: 8pt, fill: luma(100))[
  Priced as: #d.bom.lines.filter(l => l.priced_as != none).map(l => l.priced_as + " [" + l.source + "]").join("; ").
]

= Working
#for section in d.working [
  == #section.title
  #table(
    columns: (auto, auto, 1fr),
    [Step], [Result], [How],
    ..section.steps.map(s => (
      s.name,
      s.value,
      [
        #if s.formula != none [#raw(s.formula) \ ]
        #for (k, v) in s.inputs [#k: #v; ]
        #if s.note != none [\ #emph(s.note)]
        #if s.reference != none [\ #text(size: 8pt, fill: luma(100))[#s.reference]]
      ],
    )).flatten()
  )
]
