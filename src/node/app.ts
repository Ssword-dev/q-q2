import path from "node:path";
import app, { App } from "./orchestrator";

function apachePHP(app: App) {
  const apacheHttpdRootPath = path.resolve(
    process.cwd(),
    "./server/runtime/apache"
  );
  const apacheBinaryPath = path.join(apacheHttpdRootPath, "bin/httpd.exe");
  app
    .addSubprocess(apacheBinaryPath, ["-D__DEV__"])
    .addOption("cwd", apacheHttpdRootPath)
    .finalize();
}

async function main() {
  const cwd = process.cwd();
  app().apply(apachePHP).bindLifecycle();
}

main().catch(console.error);
