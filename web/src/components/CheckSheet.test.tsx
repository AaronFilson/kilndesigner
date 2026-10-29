import type { Check, Finding } from "@kilndesigner/api-client";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { CheckSheet, Maths } from "./CheckSheet";
import { Findings } from "./ReportView";

afterEach(() => {
  cleanup();
  window.history.replaceState(null, "", "/");
});

const LBF = 0.22480894309971053; // per newton
const PSI = 0.0001450377377302092; // per pascal
const IN2 = 1550.0031000062002; // per square metre

/** A rod at 2,000 lb on 0.1 in²: 20,000 psi against 12,000. */
const rod: Check = {
  id: "frame.rod",
  title: "Tie rods, hot",
  label: "E1",
  reference: "HarbisonWalker",
  cells: [
    { symbol: "P", meaning: "load on each rod", value: 2000 / LBF, label: "lbf", scale: LBF, source: "the thrust" },
    { symbol: "A_s", meaning: "stress area", value: 0.1 / IN2, label: "in²", scale: IN2, source: "the thread table" },
    { symbol: "σ", meaning: "stress", value: 20000 / PSI, label: "psi", scale: PSI, expr: "P/A_s", formula: "P/A_s" },
    { symbol: "σ_allow", meaning: "allowed", value: 12000 / PSI, label: "psi", scale: PSI },
    { symbol: "", meaning: "steel", text: "A36" },
  ],
  requirements: [
    { left: "σ", op: "<=", right: "σ_allow", level: "error", holds: false, margin: "" },
  ],
  rule_holds: true,
  rule_level: "error",
  lever: { symbol: "A_s", lo: 0.01 / IN2, hi: 1 / IN2 },
  status: "error",
  solve: "Passes when A_s ≥ 0.1667 in²",
} as Check; // prettier-ignore

describe("CheckSheet", () => {
  it("shows the formulas, the values and what would pass", () => {
    render(<CheckSheet check={rod} />);
    expect(screen.getByText("Error")).toBeTruthy();
    expect(screen.getByText("20,000 psi")).toBeTruthy();
    expect(screen.getByText("A36")).toBeTruthy();
    expect(screen.getByText(/166\.7 % of/)).toBeTruthy();
    expect(screen.getByText(/Passes when/).textContent).toBe("Passes when As ≥ 0.1667 in²");
    expect(screen.queryByText("Back to the design's values")).toBeNull();
  });

  it("recomputes from an edited input, and goes back", () => {
    render(<CheckSheet check={rod} />);
    const area = screen.getByLabelText("A_s, stress area") as HTMLInputElement;
    expect(area.value).toBe("0.1");
    fireEvent.change(area, { target: { value: "0.2" } });
    expect(screen.getByText("Passes")).toBeTruthy();
    expect(screen.getByText("10,000 psi")).toBeTruthy();
    expect(screen.getByText(/83\.33 % of/)).toBeTruthy();
    expect(screen.getByText(/Passes while/)).toBeTruthy();
    expect(screen.getByText("with your values")).toBeTruthy();
    fireEvent.change(area, { target: { value: "abc" } }); // not a number: ignored
    expect(screen.getByText("Passes")).toBeTruthy();
    fireEvent.blur(area);
    expect(area.value).toBe("0.2");
    fireEvent.click(screen.getByText("Back to the design's values"));
    expect(screen.getByText("Error")).toBeTruthy();
    expect(area.value).toBe("0.1");
  });

  it("states a rule that isn't a formula", () => {
    const ring: Check = {
      ...rod,
      cells: [{ symbol: "", meaning: "in the ring", text: "fibre blanket" } as Check["cells"][0]],
      requirements: [],
      rule: "A ring must be brick or castable.",
      rule_holds: false,
      lever: null,
      label: null,
    };
    render(<CheckSheet check={ring} />);
    expect(screen.getByText("Rule, not met:")).toBeTruthy();
    expect(screen.getByText(/A ring must be brick or castable\./)).toBeTruthy();
    expect(screen.getByText("Error")).toBeTruthy();
    cleanup();
    render(<CheckSheet check={{ ...ring, rule_holds: true, status: "pass" }} />);
    expect(screen.getByText("Rule:")).toBeTruthy();
  });
});

describe("Maths", () => {
  it("writes the part after an underscore as a subscript", () => {
    const { container } = render(<Maths text="σ = P_c/A_s + x" />);
    expect(container.innerHTML).toBe("σ = P<sub>c</sub>/A<sub>s</sub> + x");
  });
});

describe("Findings with sheets", () => {
  const finding: Finding = { level: "error", message: "The rods are overstressed.", check: rod };

  it("links each error to its sheet", () => {
    render(<Findings findings={[finding]} />);
    expect(screen.getByText("E1")).toBeTruthy();
    const why = screen.getByText("Why: the formulas and numbers");
    expect(why.getAttribute("href")).toBe("#check-frame.rod");
    fireEvent.click(why);
    expect(window.location.hash).toBe("#check-frame.rod");
    expect(screen.getByText("20,000 psi")).toBeTruthy();
    fireEvent.click(screen.getByText("Hide the working"));
    expect(screen.queryByText("20,000 psi")).toBeNull();
  });

  it("opens the sheet a shared link points to", () => {
    window.history.replaceState(null, "", "/#check-frame.rod");
    render(<Findings findings={[finding, { level: "warning", message: "No sheet." }]} />);
    expect(screen.getByText("20,000 psi")).toBeTruthy();
    expect(screen.getByText("warning")).toBeTruthy();
  });
});
