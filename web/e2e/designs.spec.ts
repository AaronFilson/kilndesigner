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

  await page.getByRole("tab", { name: "YAML" }).click();
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

test("the model is seen from each side, cut in half, and its parts named", async ({
  page,
  request,
  cleanup,
}) => {
  const id = await saved(request, cleanup, design("E2E viewer"), { built: true });
  await page.goto(`/designs/${id}`);
  const viewer = page.getByLabel("3D model of the kiln");
  await expect(viewer.locator("canvas")).toBeVisible();
  const button = (name: string) => viewer.getByRole("button", { name, exact: true });
  for (const view of ["Side", "Top", "3D", "Front"]) {
    await button(view).click();
    await expect(button(view)).toHaveAttribute("aria-pressed", "true");
  }
  await button("Cut in half").click();
  await expect(button("Cut in half")).toHaveAttribute("aria-pressed", "true");

  // From the front, the middle of the picture is a wall, door or roof layer, named in words.
  const box = await viewer.boundingBox();
  if (!box) throw new Error("no viewer");
  const status = viewer.getByRole("status");
  await expect(async () => {
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await expect(status).toContainText(/(layer \d from the inside|Element \d)/, { timeout: 1000 });
  }).toPass();
  await expect(status).not.toContainText("/"); // the title, not the part's id
});

const gasExample = readFileSync(
  new URL("../../examples/gas-crossdraft.yaml", import.meta.url),
  "utf-8",
);
const diyExample = readFileSync(
  new URL("../../examples/diy-castable-test-kiln.yaml", import.meta.url),
  "utf-8",
);

test("the model is a kiln you could build: frame, burners, chimney, coloured by material", async ({
  page,
  request,
  cleanup,
}) => {
  const source = gasExample.replace(/^name: .*$/m, `name: "E2E buildable ${Date.now()}"`);
  const id = await saved(request, cleanup, source, { built: true });
  await page.goto(`/designs/${id}`);
  const viewer = page.getByLabel("3D model of the kiln");
  await expect(viewer.locator("canvas")).toBeVisible();
  const legend = viewer.getByRole("list", { name: "Materials in the model" });
  for (const kind of ["Insulating firebrick", "Hard firebrick", "Steel", "Burners"]) {
    await expect(legend).toContainText(kind);
  }
  // Every part is named: the frame, the burners, the chimney
  const design = (await (await request.get(`/api/designs/${id}`)).json()) as {
    latest: { build_key: string };
  };
  const parts = (await (
    await request.get(`/api/builds/${design.latest.build_key}/files/parts.json`)
  ).json()) as Record<string, { title: string }>;
  const titles = Object.values(parts).map((p) => p.title);
  for (const title of ["Corner post 1 of 4", "Buttress angle, left side", "Chimney"]) {
    expect(titles).toContain(title);
  }
  expect(titles.some((t) => t.startsWith("Burner 1 of"))).toBe(true);
  await page.getByRole("tab", { name: /^Report/ }).click();
  await expect(page.getByRole("heading", { name: "Steel frame" })).toBeVisible();
});

test("a design started from a kind of kiln and edited with choices, not YAML", async ({
  page,
  cleanup,
}) => {
  const name = `E2E choices ${Date.now()}`;
  await page.goto("/designs/new");
  await page.getByRole("button", { name: /Gas cross-draft/ }).click();
  const form = page.getByRole("form", { name: "Design" });
  await form.getByLabel("Name").fill(name);
  await form.getByLabel("Width", { exact: true }).fill("30");
  await form.getByLabel("Burner type").selectOption("venturi");
  await form.getByRole("button", { name: "Add a layer to the walls" }).click();
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page).toHaveURL(/\/designs\/[0-9a-f-]{36}$/);
  cleanup(designId(page));
  await expect(page.getByRole("heading", { name })).toBeVisible();
  // The choices were saved as a design file, and YAML is still a tab away
  await expect(page.getByRole("form", { name: "Design" }).getByLabel("Width", { exact: true })).toHaveValue("30");
  await page.getByRole("tab", { name: "YAML" }).click();
  await expect(page.locator(".cm-content")).toContainText("width: 30 in");
  await expect(page.getByLabel("3D model of the kiln").locator("canvas")).toBeVisible({
    timeout: 180_000,
  });
});

test("a castable you mix: its batch, densities and first firing", async ({
  page,
  request,
  cleanup,
}) => {
  const source = diyExample.replace(/^name: .*$/m, `name: "E2E castable ${Date.now()}"`);
  const id = await saved(request, cleanup, source, { built: true });
  await page.goto(`/designs/${id}`);
  await page.getByRole("tab", { name: "Castables" }).click();
  const batch = page.getByRole("table", { name: /^One batch of Foamed fireclay backup/ });
  await expect(batch).toContainText("Greenstripe fireclay");
  await expect(page.getByText("A level US quart weighs").first()).toBeVisible();
  await expect(page.getByRole("table", { name: /^First firing of Foamed fireclay backup/ })).toContainText(
    "1000 °F",
  );
  await expect(page.getByText(/kyanite never expands/).first()).toBeVisible();
  // The form lists the mixes, and the lining can use them
  const form = page.getByRole("form", { name: "Design" });
  await expect(form.getByRole("group", { name: /^Castable: Foamed fireclay backup/ })).toBeVisible();
  await expect(form.getByLabel("Walls, layer 2 material")).toHaveValue("diy-backup");
});

test("a castable outside the checked range is refused, saying why", async ({ page, request, cleanup }) => {
  const source = diyExample
    .replace(/^name: .*$/m, `name: "E2E castable refused ${Date.now()}"`)
    .replace("foam: 55", "foam: 0");
  const id = await saved(request, cleanup, diyExample.replace(/^name: .*$/m, `name: "E2E r ${Date.now()}"`));
  await page.goto(`/designs/${id}`);
  await page.getByRole("tab", { name: "YAML" }).click();
  await page.locator(".cm-content").click();
  await page.keyboard.press("Control+A");
  await page.keyboard.insertText(source);
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page.getByRole("alert")).toContainText("480 to 1250 kg/m³");
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
