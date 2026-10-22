/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    // In development the API runs on the host: `uv run kilndesigner-api`
    proxy: { "/api": "http://127.0.0.1:8000" },
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"], // e2e/ is Playwright's
  },
});
