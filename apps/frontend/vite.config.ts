import path from "node:path";
import react from "@vitejs/plugin-react";
import { viteStaticCopy } from "vite-plugin-static-copy";
import { defineConfig } from "vitest/config";
import { playwright } from "@vitest/browser-playwright";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        {
          src: "../backend/openapi{,_spec}.json",
          dest: ".",
          rename: () => "../openapi.json",
        },
      ],
    }),
  ],
  root: import.meta.dirname,
  build: {
    // Rolldown (Vite 8's Rust bundler) bypasses Node's patched FS, so we must
    // point outDir directly at the Bazel tree-artifact path.
    // Under Bazel, CWD is already <execroot>/BAZEL_BINDIR/BAZEL_PACKAGE,
    // so "dist" relative to CWD lands in the correct tree artifact.
    outDir:
      process.env.BAZEL_BINDIR && process.env.BAZEL_PACKAGE
        ? path.resolve(process.cwd(), "dist")
        : undefined,
  },
  test: {
    retry: 3,
    setupFiles: ["./src/utils/testing-utils/setup.ts"],
    fileParallelism: false,
    browser: {
      provider: playwright({
        launchOptions: {
          args: process.env.PLAYWRIGHT_BROWSERS_PATH
            ? [
                "--no-sandbox",
                "--disable-crashpad",
                "--headless=new"
              ]
            : [],
        },
      }),
      enabled: true,
      instances: [{ browser: "chromium" }],
    },
  },
});
