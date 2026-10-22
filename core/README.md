# kilndesigner

The Kilndesigner engine: a pure Python library that turns a kiln design file into geometry, heat
loss, element and burner sizing, and plans. Every result carries its working: the inputs, the
formulas, the intermediate values and the references.

```python
from kilndesigner import load_design, design_report

kiln = load_design("kiln.yaml")
report = design_report(kiln)
print(report.heat_loss.total.to("kW"))
```

See the [project README](../README.md) for the plan and the decision records.
