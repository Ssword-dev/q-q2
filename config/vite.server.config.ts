import { defineConfig, Plugin } from "vite";
import { viteStaticCopy } from "vite-plugin-static-copy";
import dotenv from "dotenv";
import path from "path";
import { builtinModules } from "module";

// Default to development if NODE_ENV not set
const env = process.env.NODE_ENV || "development";
const envFile = path.resolve(process.cwd(), `.env.${env}`);

dotenv.config();

// Try to load .env.{NODE_ENV}
dotenv.config({ path: envFile });

const cwd = process.cwd();

// https://vite.dev/config/
export default defineConfig({
  ssr: {
    external: [],
    noExternal: true,
  },
  plugins: [
    ...viteStaticCopy({
      targets: [
        {
          src: "src/api/php",
          dest: "./api",
        },
        // copy runtimes.
        {
          src: "runtime",
          dest: ".",
        },
      ],
    }),
  ],
  build: {
    ssr: true,
    outDir: "dist/server",
    minify: true,
    rollupOptions: {
      input: {
        // server bundle. mostly just server orchestrator.
        app: path.resolve(cwd, "src/node/app.ts"),
        server: path.resolve(cwd, "src/node/server.ts"),
      },
      external: id => builtinModules.includes(id),
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "assets/[name]-[hash].js",
        format: "esm",
      },
    },
  },

  resolve: {
    alias: {
      "@": "/src/",
    },
  },
});
