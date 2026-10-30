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
  await page.keyboard.press("ControlOrMeta+End"); // CodeMirror's Mod-End: Cmd on a Mac
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

  // As a wireframe, only the parts' outlines are drawn, and a part can still be clicked and named
  await button("Wireframe").click();
  await expect(button("Wireframe")).toHaveAttribute("aria-pressed", "true");
  await page.mouse.click(box.x + 8, box.y + box.height / 2); // the background lets go of the part
  await expect(status).toContainText("Drag to turn");
  await expect(async () => {
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await expect(status).toContainText(/(layer \d from the inside|Element \d)/, { timeout: 1000 });
  }).toPass();
});

test("a peephole is added on the model where it's clicked, and taken out again", async ({
  page,
  request,
  cleanup,
}) => {
  const id = await saved(request, cleanup, design("E2E peepholes"), { built: true });
  await page.goto(`/designs/${id}`);
  const viewer = page.getByLabel("3D model of the kiln");
  const canvas = viewer.locator("canvas");
  await expect(canvas).toBeVisible();
  await page.waitForLoadState("networkidle");
  await viewer.getByRole("button", { name: "Front", exact: true }).click();
  await viewer.getByRole("button", { name: "Move ports" }).click();
  await viewer.getByLabel("Stop turning").check();
  // The camera has come round to the front once the picture stops changing
  let seen: Buffer = Buffer.alloc(0);
  await expect
    .poll(async () => {
      const now = await canvas.screenshot();
      const still = now.equals(seen);
      seen = now;
      return still;
    })
    .toBe(true);
  const box = await viewer.boundingBox();
  if (!box) throw new Error("no viewer");
  const form = page.getByRole("form", { name: "Design" });
  const rows = form.getByRole("button", { name: /^Remove spy hole \d+$/ });

  // Clicked on the front, beside the three up the door: a fourth goes there, and all are placed
  await viewer.getByRole("button", { name: "Add a peephole" }).click();
  const at = { x: box.x + box.width * 0.4, y: box.y + box.height * 0.45 };
  await page.mouse.click(at.x, at.y);
  await expect(form.getByLabel("Spy holes go")).toHaveValue("placed");
  await expect(rows).toHaveCount(4);
  await expect(form.getByLabel("Spy hole 4, wall")).toHaveValue("front");

  // Clicked again, it's picked, and taken out
  await page.mouse.click(at.x, at.y);
  await viewer.getByRole("button", { name: "Remove peephole 4" }).click();
  await expect(rows).toHaveCount(3);
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
  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.insertText(source);
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page.getByRole("alert")).toContainText("480 to 1250 kg/m³");
});

test("the app and the model take the colours chosen, and keep them", async ({
  page,
  request,
  cleanup,
}) => {
  const id = await saved(request, cleanup, design("E2E colours"), { built: true });
  await page.goto(`/designs/${id}`);
  await page.getByLabel("Theme").selectOption("dark");
  await page.getByLabel("Accent colour").selectOption("cobalt");
  const root = page.locator("html");
  await expect(root).toHaveAttribute("data-theme", "dark");
  await expect(root).toHaveAttribute("data-accent", "cobalt");

  const viewer = page.getByLabel("3D model of the kiln");
  await expect(viewer.locator("canvas")).toBeVisible();
  await viewer.getByLabel("Model colours").selectOption("blueprint");
  await viewer.getByRole("button", { name: "Outlines" }).click();
  await expect(viewer.getByRole("button", { name: "Outlines" })).toHaveAttribute("aria-pressed", "true");
  const swatch = viewer.getByLabel("Colour for Insulating firebrick");
  await expect(swatch).toHaveValue("#d6e6f5"); // the blueprint's
  await swatch.fill("#ff00ff");

  await page.reload();
  await expect(root).toHaveAttribute("data-theme", "dark");
  await expect(viewer.getByLabel("Model colours")).toHaveValue("blueprint");
  await expect(viewer.getByLabel("Colour for Insulating firebrick")).toHaveValue("#ff00ff");
  await viewer.getByRole("button", { name: "Reset colours" }).click();
  await expect(viewer.getByLabel("Colour for Insulating firebrick")).toHaveValue("#d6e6f5");
});

/** The latest build's layout.json: where each port was cut. */
async function layoutOf(request: APIRequestContext, id: string) {
  const d = (await (await request.get(`/api/designs/${id}`)).json()) as {
    latest: { number: number; build_key: string };
  };
  const response = await request.get(`/api/builds/${d.latest.build_key}/files/layout.json`);
  if (!response.ok()) return null;
  return (await response.json()) as { ports: { name: string; wall: string; across: number }[] };
}

test("a burner port dragged on the model is placed there, saved and built there", async ({
  page,
  request,
  cleanup,
}) => {
  const source = gasExample.replace(/^name: .*$/m, `name: "E2E move ports ${Date.now()}"`);
  const id = await saved(request, cleanup, source, { built: true });
  await page.goto(`/designs/${id}`);
  const viewer = page.getByLabel("3D model of the kiln");
  await expect(viewer.locator("canvas")).toBeVisible();
  await page.waitForLoadState("networkidle");
  await viewer.getByRole("button", { name: "Front", exact: true }).click();
  await viewer.getByRole("button", { name: "Move ports" }).click();
  await viewer.getByLabel("Stop turning").check();

  // The markers are drawn in the model: find burner port 1 by pointing at it
  const box = await viewer.boundingBox();
  if (!box) throw new Error("no viewer");
  const status = viewer.getByRole("status");
  let at: { x: number; y: number } | null = null;
  // Up and down each column, out from the middle where the example's one port is: a sweep row by
  // row took too long for CI's 3 minutes
  const offsets = [0];
  for (let dx = 0.01; dx < 0.3; dx += 0.01) offsets.push(dx, -dx);
  for (const dx of offsets) {
    for (let y = 0.95; y > 0.3 && !at; y -= 0.015) {
      const x = 0.5 + dx;
      await page.mouse.move(box.x + box.width * x, box.y + box.height * y);
      if ((await status.textContent())?.startsWith("Burner port 1")) {
        at = { x: box.x + box.width * x, y: box.y + box.height * y };
      }
    }
    if (at) break;
  }
  expect(at, "burner port 1's marker").not.toBeNull();

  // With turning stopped, a drag that misses every port leaves the model as it was
  const model = () =>
    viewer.locator("canvas").screenshot({
      mask: [viewer.getByRole("toolbar"), status, viewer.locator(".viewer-legend")],
    });
  const off = { x: box.x + box.width * 0.1, y: box.y + box.height * 0.5 };
  await page.mouse.move(off.x, off.y); // off the ports first, so the status is the same after
  const before = await model();
  await page.mouse.down();
  for (let i = 1; i <= 8; i++) await page.mouse.move(off.x + i * 12, off.y);
  await page.mouse.up();
  expect((await model()).equals(before), "the model didn't turn").toBe(true);

  await page.mouse.move(at!.x, at!.y);
  await page.mouse.down();
  for (let i = 1; i <= 8; i++) await page.mouse.move(at!.x + i * 4, at!.y - i * 4);
  await page.mouse.up();

  // The form now places each burner, the first where it was dropped
  const form = page.getByRole("form", { name: "Design" });
  await expect(form.getByLabel("Burner ports go")).toHaveValue("placed");
  const across = form.getByLabel("Burner 1, across", { exact: true });
  await expect(across).not.toHaveValue("-7");
  const dropped = Number(await across.inputValue());
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page.locator(".toolbar > .muted")).toHaveText("Version 2");
  await expect
    .poll(async () => (await layoutOf(request, id))?.ports.find((p) => p.name === "port/burner-1")?.across, {
      timeout: 180_000,
    })
    .toBeCloseTo(dropped * 25.4, 1);
});

const catenaryExample = readFileSync(
  new URL("../../examples/catenary-gas-kiln.yaml", import.meta.url),
  "utf-8",
);
const domeExample = readFileSync(
  new URL("../../examples/dome-castable-kiln.yaml", import.meta.url),
  "utf-8",
);

for (const [kind, example, arch, holds] of [
  ["catenary arch", catenaryExample, "Catenary arch, layer 1 from the inside", /pushes out with/],
  ["dome", domeExample, "Roof, layer 1 from the inside", /No source sizes the steel for a dome/],
] as const) {
  test(`a ${kind} is built, named, drawn and its thrust spoken for`, async ({
    page,
    request,
    cleanup,
  }) => {
    const source = example.replace(/^name: .*$/m, `name: "E2E ${kind} ${Date.now()}"`);
    const id = await saved(request, cleanup, source, { built: true });
    const d = (await (await request.get(`/api/designs/${id}`)).json()) as {
      latest: { build_key: string };
    };
    const parts = (await (
      await request.get(`/api/builds/${d.latest.build_key}/files/parts.json`)
    ).json()) as Record<string, { title: string }>;
    expect(Object.values(parts).map((p) => p.title)).toContain(arch);

    await page.goto(`/designs/${id}`);
    const viewer = page.getByLabel("3D model of the kiln");
    await expect(viewer.locator("canvas")).toBeVisible();
    await page.waitForLoadState("networkidle");
    await expect(viewer.getByRole("alert")).toHaveCount(0);
    await page.getByRole("tab", { name: "Drawings" }).click();
    await expect(page.getByRole("img", { name: /^Section A–A/ })).toBeVisible();
    await page.getByRole("tab", { name: /^Report/ }).click();
    await expect(page.getByText(holds).first()).toBeVisible();
  });
}

test("a kiln is given a catenary arch with choices, and its door moves off the side", async ({
  page,
  cleanup,
}) => {
  const name = `E2E catenary choice ${Date.now()}`;
  await page.goto("/designs/new");
  await page.getByRole("button", { name: /Gas cross-draft/ }).click();
  const form = page.getByRole("form", { name: "Design" });
  await form.getByLabel("Name").fill(name);
  const roof = form.locator("label.field").filter({ has: page.getByText("Roof", { exact: true }) });
  await roof.locator("select").selectOption("catenary_arch");
  await expect(form.getByLabel("Height, to the crown", { exact: true })).toBeVisible();
  await expect(form.getByLabel("The door's wall")).not.toHaveValue(/left|right/);
  await page.getByRole("button", { name: "Save and build" }).click();
  await expect(page).toHaveURL(/\/designs\/[0-9a-f-]{36}$/);
  cleanup(designId(page));
  await page.getByRole("tab", { name: "YAML" }).click();
  await expect(page.locator(".cm-content")).toContainText("type: catenary_arch");
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
