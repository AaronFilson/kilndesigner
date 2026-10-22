// End-to-end tests: a real browser against a running app. Start it with `docker compose up`, or
// point KILNDESIGNER_E2E_URL at the dev loop (http://localhost:5173). They drive the installed
// Google Chrome, so there is no browser to download.
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  timeout: 180_000, // designs are built on the worker; the first build after a start is slowest
  expect: { timeout: 15_000 },
  forbidOnly: !!process.env.CI,
  outputDir: "../test-results",
  reporter: process.env.CI
    ? [["list"], ["html", { open: "never", outputFolder: "../playwright-report" }]]
    : "list",
  use: {
    baseURL: process.env.KILNDESIGNER_E2E_URL ?? "http://localhost:8080",
    channel: "chrome",
    trace: "retain-on-failure",
  },
});
