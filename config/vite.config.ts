import { defineConfig, Plugin } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import glsl from "vite-plugin-glsl";
import dotenv from "dotenv";
import path from "path";

// Default to development if NODE_ENV not set
const env = process.env.NODE_ENV || "development";
const envFile = path.resolve(process.cwd(), `.env.${env}`);

dotenv.config();

// Try to load .env.{NODE_ENV}
dotenv.config({ path: envFile }
);

const cwd = process.cwd();

// https://vite.dev/config/
export default defineConfig({
  base: process.env.DIST_BASE_PATH || "/",
  plugins: [
    glsl({
      importKeyword: "include",
    }),
    tailwindcss(),
    react(),
  ],
  build: {
    rollupOptions: {
      input: {
        calendar: path.resolve(cwd, "calendar.html"),
        main: path.resolve(cwd, "index.html"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "assets/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          console.log(assetInfo.names[0])
          if (/\.html$/.test(assetInfo.names[0])) {
            return "[name].html"; // makes sure html files are built using the name.
          }
          return "assets/[name]-[hash][extname]";
        },
      }
    },
  },

  resolve: {
    alias: {
      "@": "/src/",
    },
  },
});
