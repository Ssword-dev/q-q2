import path from "path";
import fsx from "fs-extra";
import express from "express";
import { createServer as createViteServer } from "vite";
import { spawn } from "child_process";

async function main() {
  const cwd = process.cwd();
  const viteConfig = path.resolve(cwd, "./config/vite.config.ts");
  const apacheHttpdRootPath = path.resolve(cwd, "./runtime/apache");
  const apacheBinaryPath = path.resolve(apacheHttpdRootPath, "./bin/httpd.exe");

  const app = express();

  const vite = await createViteServer({
    configFile: viteConfig,
    server: {
      middlewareMode: true,
    },
  });

  app.use(vite.middlewares);

  const apache = spawn(apacheBinaryPath, ["-D", "__DEV__"], {
    stdio: "inherit",
    cwd: apacheHttpdRootPath,
  });

  const server = app.listen(4000, "127.0.0.1");

  const cleanup = async () => {
    apache.kill("SIGINT");

    const apachePIDFile = path.resolve(apacheHttpdRootPath, "./logs/httpd.pid");

    const apacheDidNotCleanUp = await fsx.pathExists(apachePIDFile);

    if (apacheDidNotCleanUp) {
      await fsx.remove(apachePIDFile);
    }

    server.close();
    process.exit();
  };

  process.on("SIGINT", cleanup).on("SIGTERM", cleanup);
}

main().catch(console.error);
