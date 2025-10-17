// import path from "node:path";

import path from "path";
import fs, { access, constants } from "fs/promises";
import express from "express";
import { createServer as createViteServer } from "vite";
import { spawn, SpawnOptions } from "child_process";

function spawnPromise(
  command: string,
  args: readonly string[],
  options: SpawnOptions
) {
  return new Promise((resolve, reject) => {
    let output = "";

    const proc = spawn(command, args, {
      stdio: "pipe",
    });

    proc.stdout.on("data", data => {
      output += data.toString();
    });

    proc.stderr.on("data", data => {
      output += data.toString();
    });

    proc.on("exit", code => {
      if (code === 0) {
        resolve(output);
      } else {
        reject(
          new Error(output.trim() || `${command} ${args.join(" ")} failed`)
        );
      }
    });

    proc.on("error", err => {
      reject(err);
    });
  });
}

async function fileExists(path: string) {
  try {
    await access(path, constants.F_OK);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  const cwd = process.cwd();
  const viteConfig = path.resolve(cwd, "./config/vite.client.config.ts");
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

    const apacheDidNotCleanUp = await fileExists(apachePIDFile);

    if (apacheDidNotCleanUp) {
      fs.unlink(apachePIDFile);
    }

    server.close();
    process.exit();
  };

  process.on("SIGINT", cleanup).on("SIGTERM", cleanup);
}

main().catch(console.error);
