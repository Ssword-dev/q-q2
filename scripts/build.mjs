// @ts-ignore
// eslint-disable

import { fileURLToPath } from "node:url";
import path from "node:path";
import fsx from "fs-extra";
import { build } from "vite";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const __project = path.dirname(__dirname); // step 1 back.
const __configDirectory = path.resolve(__project, "./config");
const __sourceDirectory = path.resolve(__project, "./src");
const __distDirectory = path.resolve(__project, "./dist");

// emojis.

const emojiPreset = {
  check: "✅",
  warn: "⚠️",
  X: "❌",
  yippee: "🎉",
};

const emojis = {
  frontendBuilt: emojiPreset.check,
  scriptsBuilt: emojiPreset.check,
  apiCopied: emojiPreset.check,
  runtimeLogsCleaned: emojiPreset.check,
  runtimeSetupBuilt: emojiPreset.check,
  apiMissing: emojiPreset.warn,
  fatalError: emojiPreset.X,
  buildFailed: emojiPreset.X,
  buildDone: emojiPreset.yippee,
};

class BuildError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

async function buildFrontend() {
  const viteConfig = path.resolve(__configDirectory, "./vite.config.ts");

  await build({
    configFile: viteConfig,
  });
}

function createLogFileCleaner(runtimeDist) {
  const runtimeApacheRoot = path.resolve(runtimeDist, "./apache");
  return async function logFileCleaner(logFile) {
    const absPath = path.resolve(runtimeApacheRoot, logFile);
    const logFileExists = await fsx.pathExists(absPath);

    if (logFileExists) {
      await fsx.truncate(absPath, 0); // clear the log file.
    } else {
      await fsx.createFile(absPath);
    }
  };
}

async function buildAPI() {
  const apiSource = path.resolve(__sourceDirectory, "./api");

  // copy the api

  try {
    await fsx.exists(apiSource);
  } catch (_) {
    console.log("api source does not exist... skipping api build step...");
    return;
  }

  const apiDist = path.resolve(__distDirectory, "./api");

  await fsx.copy(apiSource, apiDist);

  console.log(`${emojis.apiCopied} api source sucessfully built!.`);
}

async function buildRuntime() {
  const runtimeSource = path.resolve(__project, "./runtime");
  const runtimeDist = path.resolve(__distDirectory, "./runtime");

  try {
    await fsx.exists(runtimeSource);
  } catch (_) {
    throw new BuildError(`${emojis.fatalError} runtime does not exist.`);
  }

  await fsx.copy(runtimeSource, runtimeDist);

  // truncate the logs from development.
  const logFileCleaner = createLogFileCleaner(runtimeDist);
  const logFiles = ["logs/access.log", "logs/error.log", "logs/install.log"];

  // process log file truncation in parallel.
  await Promise.all(logFiles.map(lf => logFileCleaner(lf)));
  console.log(
    `${emojis.runtimeLogsCleaned} runtime logs successfully cleaned.`
  );

  const httpdProcessIdFile = path.resolve(runtimeDist, "logs/httpd.pid");
  const httpdProcessIdFileExists = await fsx.exists(httpdProcessIdFile);

  if (httpdProcessIdFileExists) {
    await fsx.remove(httpdProcessIdFile);
  }

  // create cache directory
  const cacheRootDirectory = path.resolve(runtimeDist, "./apache/cache");

  await fsx.ensureDir(cacheRootDirectory);

  console.log(`${emojis.runtimeSetupBuilt} runtime setup successfully built!`);
}

async function buildScripts() {
  const startScriptContent = `
@echo off
:: do not edit this script. this is auto-generated.
set "BUILD=%~dp0"

:: make sure the cwd is the apache root folder.
cd /d "%BUILD%\\runtime\\apache"

start "" ".\\bin\\httpd.exe" -D __PROD__ >nul 2>&1

exit
    `;

  const stopScriptContent = `
@echo off
:: do not edit this script. this is auto-generated.
set "BUILD=%~dp0"

:: make sure the cwd is the apache root folder.
cd /d "%BUILD%\\runtime\\apache"

set "PID_FILE=%BUILD%\\runtime\\apache\\logs\\httpd.pid"

:: read the first line of the file into variable APACHE_PID
set /p APACHE_PID=<"%PID_FILE%"

if not defined APACHE_PID (
    echo "apache was not running."
    exit
)

:: kill apache. forcefully.

taskkill /PID "%APACHE_PID" /F >nul 2>&1

:: delete possible pid remnant.

if exist "%PID_FILE%" (
    del "%PID_FILE%"
)
    `;

  const startScript = path.resolve(__distDirectory, "./start.cmd");
  const stopScript = path.resolve(__distDirectory, "./stop.cmd");

  await fsx.writeFile(startScript, startScriptContent.trim());
  await fsx.writeFile(stopScript, stopScriptContent.trim());

  console.log(`${emojis.scriptsBuilt} scripts succesfully built!`);
}

async function main() {
  // the frontend is required to be built first so dist/ gets created.
  await buildFrontend();

  // all these are executed concurrently because
  // they do not depend on order.
  await Promise.all([buildAPI(), buildRuntime(), buildScripts()]);
  console.log(`${emojis.buildDone} Build done!`);
}

main().catch(err => {
  if (err instanceof BuildError) {
    console.error(err.message);
    process.exit(1);
  } else {
    console.error(`Internal build error: ${err.message}.`);
  }
});
