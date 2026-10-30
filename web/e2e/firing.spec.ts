// A firing, in a real browser: build a design, simulate its firing on the worker, read the charts
// and scrub the walls' heatmap through time.
import { readFileSync } from "node:fs";

import type { Build } from "@kilndesigner/api-client";
import { expect, test } from "@playwright/test";

const example = readFileSync(new URL("../../examples/electric-front-loader.yaml", import.meta.url), "utf-8");

test("a design's firing is simulated, charted and shown as a heatmap", async ({ page, request }) => {
  const problems: string[] = [];
  page.on("pageerror", (e) => problems.push(e.message));
  const source = example.replace(/^name: .*$/m, `name: "E2E firing ${Date.now()}"`);
  const response = await request.post("/api/designs", { data: { source } });
  expect(response.status()).toBe(201);
  const { id, latest } = (await response.json()) as { id: string; latest: { build_key: string } };
  try {
    const build = `/api/builds/${latest.build_key}`;
    await request.post(build);
    const status = async () => ((await (await request.get(build)).json()) as Build).status;
    await expect.poll(status, { timeout: 180_000 }).toBe("done");

    await page.goto(`/designs/${id}`);
    await page.getByRole("tab", { name: "Firing" }).click();
    await page.getByRole("button", { name: "Simulate the firing" }).click();

    // The figures and the charts, once the worker has fired it
    await expect(page.getByText("Schedule kept")).toBeVisible({ timeout: 120_000 });
    await expect(page.getByRole("img", { name: "Temperature" })).toBeVisible();
    await expect(page.getByRole("img", { name: "Energy and cost" })).toBeVisible();
    await expect(page.locator(".heatmap-canvas canvas")).toBeVisible();

    // Scrub back to the start: the walls are cold
    const slider = page.getByRole("slider", { name: "Time through the firing" });
    await slider.fill("0");
    await expect(page.getByText("0 h 00 min").first()).toBeVisible();
    const hotFaces = page.getByRole("table").getByRole("row").nth(1).getByRole("cell").nth(1);
    await expect(hotFaces).toHaveText(/^2\d °C$/);
    expect(problems).toEqual([]);
  } finally {
    await request.delete(`/api/designs/${id}`);
  }
});
