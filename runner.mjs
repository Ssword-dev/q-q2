import path from "node:path";

import { createServer } from "vite";
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

async function main() {
  const cwd = process.cwd();
  const app = express();
  const viteServer = await createServer({
    server: {
      middlewareMode: true,
    },
  });

  // !! THIS ASSUMES THE PROJECT FOLDER IS PLACED AT
  // !! C:\\wamp64(_\d)?\\www\\
  const project = path.basename(cwd);

  if (process.env.NODE_ENV === "development") {
    app.use(
      "/api/",
      createProxyMiddleware({
        target: "http://localhost", // Listen to WAMP's apache.
        changeOrigin: true,
        pathRewrite: (p) => p.replace(/^\/(.+)/, `/${project}/public/api/$1`),
      })
    );

    app.use(viteServer.middlewares);
  }

  viteServer.bindCLIShortcuts({
    print: true,
  });

  app.listen(4000, "0.0.0.0");
}

main().catch(console.error);
