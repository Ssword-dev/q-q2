import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import dotenv from "dotenv";
import path from "path";

// Default to development if NODE_ENV not set
const env = process.env.NODE_ENV || "development";
const envFile = path.resolve(process.cwd(), `.env.${env}`);

dotenv.config();

// Try to load .env.{NODE_ENV}
dotenv.config({ path: envFile });

const cwd = process.cwd();

// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), react()],
  build: {
    outDir: "dist/app",
    minify: true,
    cssMinify: true,
    rollupOptions: {
      input: {
        calendar: path.resolve(cwd, "calendar.html"),
        main: path.resolve(cwd, "index.html"),
      },
      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "assets/[name]-[hash].js",
      },
    },
  },

  resolve: {
    alias: {
      "@": "/src/",
    },
  },
});
