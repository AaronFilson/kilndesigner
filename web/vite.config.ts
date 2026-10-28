/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const secondPort = process.env.KILNDESIGNER_WEB_PORT;

export default defineConfig({
  plugins: [react()],
  // A second dev loop pre-bundles its dependencies into its own folder. Sharing one, a server
  // links chunks the other has replaced, and the 3D viewer gets two copies of React Three Fiber.
  cacheDir: secondPort ? `node_modules/.vite-${secondPort}` : undefined,
  server: {
    // In development the API runs on the host: `uv run kilndesigner-api`. KILNDESIGNER_API and
    // KILNDESIGNER_WEB_PORT run a second dev loop beside the first, against another API.
    proxy: { "/api": process.env.KILNDESIGNER_API ?? "http://127.0.0.1:8000" },
    port: Number(secondPort ?? 5173),
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"], // e2e/ is Playwright's
  },
});
