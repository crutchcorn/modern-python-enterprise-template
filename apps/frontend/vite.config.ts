import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { viteStaticCopy } from "vite-plugin-static-copy";

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
});
