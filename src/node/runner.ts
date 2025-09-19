// import path from "node:path";

import path from "path";
import app from "./app";

// import { createServer } from "vite";
// import express from "express";
// import { createProxyMiddleware } from "http-proxy-middleware";

// async function main() {
//   const cwd = process.cwd();
//   const app = express();
//   const viteServer = await createServer({
//     server: {
//       middlewareMode: true,
//     },
//   });

//   // !! THIS ASSUMES THE PROJECT FOLDER IS PLACED AT
//   // !! C:\\wamp64(_\d)?\\www\\
//   const project = path.basename(cwd);

//   if (process.env.NODE_ENV === "development") {
//     app.use(
//       "/api/",
//       createProxyMiddleware({
//         target: "http://localhost", // Listen to WAMP's apache.
//         changeOrigin: true,
//         pathRewrite: (p) => p.replace(/^\/(.+)/, `/${project}/public/api/$1`),
//       })
//     );

//     app.use(viteServer.middlewares);
//   }

//   viteServer.bindCLIShortcuts({
//     print: true,
//   });

//   app.listen(4000, "0.0.0.0");
// }

async function main() {
  const cwd = process.cwd();
  const project = path.basename(cwd);

  await app()
    .ifDev((app) => {
      const pythonServerPath = path.resolve(cwd, "./src/python/main.py");
      app
        .addService("wampapache64")
        .finalize()
        .use((_) => console.log("Spawned wampapache64"))
        .addSubprocess("python", [pythonServerPath])
        .addOption("stdio", "inherit")
        .finalize()
        .addProxy("/api/php/", {
          target: "http://localhost", // Listen to WAMP's apache.
          changeOrigin: true,
          pathRewrite: (p) => p.replace(/^\/(.+)/, `/${project}/public/api/$1`),
        })
        .addProxy("/api/python", {
          target: "http://localhost:5000", // Listen to flask server. mostly for holidays.
          changeOrigin: true,
          pathRewrite: (p) => p.replace(/^\/(.+)/, `/api/$1`),
        })
        .addVite({})
        .use((_) => {
          console.log("Finished configuring app for development!");
        });
    })
    .listen(4000, "0.0.0.0")
    .promise();
}

main().catch(console.error);
