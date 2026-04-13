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
});
