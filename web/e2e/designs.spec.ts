// A potter's way through the app, in a real browser: open a design file, save it, watch it build,
// look at the model and the report, edit it, and recover when something fails.
import { readFileSync } from "node:fs";

import type { Build } from "@kilndesigner/api-client";
import { type APIRequestContext, test as base, expect, type Page } from "@playwright/test";

const example = readFileSync(
  new URL("../../examples/electric-front-loader.yaml", import.meta.url),
  "utf-8",
);

/** The example under another name. The name is part of the design, so it gets its own build. */
function design(name: string): string {
  return example.replace(/^name: .*$/m, `name: ${JSON.stringify(name)}`);
}

function file(source: string) {
  return { name: "kiln.yaml", mimeType: "text/yaml", buffer: Buffer.from(source) };
}

function designId(page: Page): string {
  const id = /\/designs\/([0-9a-f-]{36})$/.exec(page.url())?.[1];
  if (!id) throw new Error(`not a design page: ${page.url()}`);
  return id;
}

const test = base.extend<{
  /** Fails the test on an uncaught error in the page or a server error, unless it is allowed. */
  pageProblems: { allow: (url: RegExp) => void };
  /** Designs the test made, deleted after it. */
  cleanup: (id: string) => void;
}>({
  pageProblems: [
    async ({ page }, use) => {
      const problems: string[] = [];
      const allowed: RegExp[] = [];
      page.on("pageerror", (e) => problems.push(`uncaught: ${e.message}`));
      page.on("response", (r) => {
        if (r.status() >= 500 && !allowed.some((url) => url.test(r.url()))) {
          problems.push(`${r.status()} from ${r.url()}`);
        }
      });
      await use({ allow: (url) => allowed.push(url) });
      expect(problems).toEqual([]);
    },
    { auto: true },
  ],
  cleanup: async ({ request }, use) => {
    const ids: string[] = [];
    await use((id) => ids.push(id));
    for (const id of ids) await request.delete(`/api/designs/${id}`);
  },
});

/** Save a design and start its build through the API, for tests about what comes after. */
async function saved(
  request: APIRequestContext,
  cleanup: (id: string) => void,
  source: string,
  { built = false } = {},
) {
  const response = await request.post("/api/designs", { data: { source } });
  expect(response.status()).toBe(201);
  const { id, latest } = (await response.json()) as { id: string; latest: { build_key: string } };
  cleanup(id);
  const build = `/api/builds/${latest.build_key}`;
  await request.post(build);
  if (built) {
    const status = async () => ((await (await request.get(build)).json()) as Build).status;
    await expect.poll(status, { timeout: 180_000 }).toBe("done");
  }
  return id;
}

test("a design opened from a file is saved, built on the worker and shown", async ({
  page,
  cleanup,
}) => {
  const name = `E2E new design ${Date.now()}`; // a new name, so a new build
  await page.goto("/");
  await page.getByRole("link", { name: "New design" }).click();
  await expect(page.getByRole("heading", { name: "New design" })).toBeVisible();

  await page.getByLabel("Open a design file").setInputFiles(file(design(name)));
  await expect(page.locator(".cm-content")).toContainText("chamber:");
  const model = page.waitForResponse((r) => r.url().endsWith("/files/kiln.glb") && r.ok(), {
    timeout: 180_000,
  });
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page).toHaveURL(/\/designs\/[0-9a-f-]{36}$/);
  cleanup(designId(page));
  await expect(page.getByRole("heading", { name })).toBeVisible();

  await model;
  const viewer = page.getByLabel("3D model of the kiln");
  await expect(viewer.locator("canvas")).toBeVisible();
  await page.waitForLoadState("networkidle");
  await expect(viewer.getByRole("alert")).toHaveCount(0);

  await page.getByRole("tab", { name: "Drawings" }).click();
  const section = page.getByRole("img", { name: /^Section A–A/ });
  await expect(section).toBeVisible();
  expect(await section.evaluate((img: HTMLImageElement) => img.naturalWidth)).toBeGreaterThan(0);
  await expect(page.getByRole("heading", { name: "Course plans" })).toBeVisible();

  await page.getByRole("tab", { name: "Materials" }).click();
  const bom = page.getByRole("table", { name: "Bill of materials" });
  await expect(bom).toContainText("Total of the priced items");
  await expect(page.getByRole("table", { name: "Cut list" })).toBeVisible();

  await page.getByRole("tab", { name: /^Report/ }).click();
  await expect(page.getByRole("heading", { name: "Heat loss" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Elements" })).toBeVisible();
  await expect(page.getByText("Electrical work must follow your local code")).toBeVisible();

  const download = page.waitForEvent("download");
  await page.getByRole("link", { name: "Plans (PDF)" }).click();
  expect((await download).suggestedFilename()).toBe("plans.pdf");

  await page.getByRole("link", { name: "Kilndesigner" }).click();
  await expect(page.getByRole("link", { name })).toBeVisible();
});

test("a design that isn't valid is refused, showing where it's wrong", async ({ page }) => {
  await page.goto("/designs/new");
  const open = page.getByLabel("Open a design file");
  const save = page.getByRole("button", { name: "Save and build" });

  await open.setInputFiles(file(example.replace(/^chamber:\n(?: {2}.*\n)+/m, "")));
  await save.click();
  await expect(page.getByRole("alert")).toContainText("chamber");

  await open.setInputFiles(file("name: [unclosed\n"));
  await save.click();
  await expect(page.getByRole("alert")).toContainText("not valid YAML");
  await expect(page).toHaveURL(/\/designs\/new$/);
});

test("saving an edit adds a version, and an earlier version can be loaded back", async ({
  page,
  request,
  cleanup,
}) => {
  await page.goto(`/designs/${await saved(request, cleanup, design("E2E versions"))}`);
  const status = page.locator(".toolbar > .muted");
  await expect(status).toHaveText("Version 1");

  await page.locator(".cm-content").click();
  await page.keyboard.press("Control+End");
  await page.keyboard.insertText("# Edited in the browser\n");
  await expect(status).toHaveText("Version 1 · unsaved changes");
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(status).toHaveText("Version 2");

  const history = page.getByLabel("Load an earlier version into the editor");
  await expect(history.locator("option")).toHaveCount(3); // the prompt and two versions
  await history.selectOption("1");
  await expect(status).toHaveText("Version 2 · unsaved changes");
});

test("a model that can't be loaded leaves the rest of the page working", async ({
  page,
  request,
  cleanup,
  pageProblems,
}) => {
  pageProblems.allow(/\/files\/kiln\.glb$/);
  await page.route("**/files/kiln.glb", (route) =>
    route.fulfill({ status: 500, body: "Internal Server Error" }),
  );
  const id = await saved(request, cleanup, design("E2E model fails"), { built: true });
  await page.goto(`/designs/${id}`);

  await expect(page.getByText("The 3D model could not be shown")).toBeVisible();
  await expect(page.getByRole("heading", { name: "E2E model fails" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Plans (PDF)" })).toBeVisible();
  await page.getByRole("tab", { name: /^Report/ }).click();
  await expect(page.getByRole("heading", { name: "Heat loss" })).toBeVisible();
});
