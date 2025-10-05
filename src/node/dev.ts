// import path from "node:path";

import path from "path";
import app from "./orchestrator/index";
import routes from "./routes";

async function main() {
  const cwd = process.cwd();
  const project = path.basename(cwd);
  const viteConfig = path.resolve(cwd, "./config/vite.client.config.ts");

  await app()
    .express()
    .apply(routes)
    .addService("wampapache64")
    .finalize()
    .addService("wampmariadb64")
    .finalize()
    .addService("wampmysqld64")
    .finalize()
    .proxy("/api/php/", {
      target: "http://localhost", // Listen to WAMP's apache.
      changeOrigin: true,
      pathRewrite: p => p.replace(/^\/(.+)/, `/${project}/src/api/php/$1`),
    })
    .addVite({
      configFile: viteConfig,
    })
    .apply(_ => {
      console.log("Finished configuring app for development!");
    })
    .listen(4000, "0.0.0.0")
    .bindLifecycle()
    .promise();
}

main().catch(console.error);
