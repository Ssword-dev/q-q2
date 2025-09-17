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

// https://vite.dev/config/
export default defineConfig({
  base: process.env.DIST_BASE_PATH || "/",
  plugins: [tailwindcss(), react()],
  build: {
    rollupOptions: {
      input: {
        calendar: "calendar.html",
      },
    },
  },

  resolve: {
    alias: {
      "@": "/src/",
    },
  },
});
