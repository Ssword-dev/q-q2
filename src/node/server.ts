import path from "node:path";
import app, { App } from "./orchestrator";
import routes from "./routes";

function apachePHP(app: App) {
  const apacheHttpdRootPath = path.resolve(
    process.cwd(),
    "./server/runtime/apache"
  );
  const apacheBinaryPath = path.join(apacheHttpdRootPath, "bin/httpd.exe");
  app
    .addSubprocess(apacheBinaryPath, [])
    .addOption("cwd", apacheHttpdRootPath)
    .finalize()
    .proxy("/api/php", {
      target: "http://localhost:4001",
      changeOrigin: true,
      pathRewrite: path => path.replace(/^\/api\/php/, ""),
    });
}

async function main() {
  const cwd = process.cwd();
  const clientRoot = path.resolve(cwd, "app");
  app()
    .apply(apachePHP)
    .apply(routes)
    .static("/", clientRoot)
    .bindLifecycle()
    .listen(80, "0.0.0.0");
}

main().catch(console.error);
