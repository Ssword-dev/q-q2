// import path from "node:path";

import path from "path";
import app, { App } from "./app";
import os from "node:os";
import express from "express";
import Holidays from "date-holidays";

function indent(s: string, spaces: number) {
  return " ".repeat(spaces) + s;
}

function formatDate(d: Date) {
  const month = d.getMonth() + 1; // getMonth returns 0 for january, ..., so need + 1 because off by one.
  const day = d.getDate(); // weirdly, this does not start with 0.
  return `${d.getFullYear()}-${month > 9 ? month : `0${month}`}-${day > 9 ? day : `0${day}`}`; // as YY-MM-DD format.
}

function applyRoutes(app: App) {
  async function handleHolidaysRoute(
    req: express.Request<
      { year: number; country: string },
      any,
      any,
      {
        state?: string;
      }
    >,
    res: express.Response
  ) {
    const { year, country } = req.params;
    const { state } = req.query;

    // build holidays object.
    const holidays = new Holidays({
      country,
      state: state,
    });

    // actual holidays.
    const actualHolidaysData = holidays.getHolidays(year);

    // map to date: rest of object.
    const holidayMappings = Object.fromEntries(
      actualHolidaysData.map(({ date: _, rule: __, start, end: ___, ...h }) => [
        formatDate(start),
        h,
      ])
    );

    // construct actual response.
    const response = {
      year,
      country,
      state,
      holidays: holidayMappings,
    };

    res.json(response);
  }

  app.get(
    "/api/node/holidays/:year/:country",
    // decay the type down to an ordinary request handler
    handleHolidaysRoute as unknown as express.RequestHandler
  );

  // function is applied.
}

async function main() {
  const cwd = process.cwd();
  const project = path.basename(cwd);
  const viteConfig = path.resolve(cwd, "./config/vite.config.ts");

  await app()
    .ifDev(app => {
      const pythonServerPath = path.resolve(cwd, "./src/python/main.py");
      app
        .addService("wampapache64")
        .finalize()
        .addService("wampmariadb64")
        .finalize()
        .addService("wampmysqld64")
        .finalize()
        .apply(_ => console.log("Spawned wampapache64"))
        .addSubprocess("python", [pythonServerPath])
        .addOption("stdio", "inherit")
        .finalize()
        .apply(applyRoutes)
        .addProxy("/api/php/", {
          target: "http://localhost", // Listen to WAMP's apache.
          changeOrigin: true,
          pathRewrite: p => p.replace(/^\/(.+)/, `/${project}/public/api/$1`),
        })
        // no need to add proxy to node. node itself is the process.
        // .addProxy("/api/python/", {
        //   target: "http://localhost:5000", // Listen to flask server. mostly for holidays.
        //   changeOrigin: true,
        //   pathRewrite: p => p.replace(/^\/(.+)/, `/api/$1`),
        // })
        .addVite({
          configFile: viteConfig,
        })
        .apply(_ => {
          console.log("Finished configuring app for development!");
        });
    })
    .listen(4000, "0.0.0.0")
    .apply(app => {
      const nets = os.networkInterfaces();

      console.log("Server is available at:");

      for (const name of Object.keys(nets)) {
        for (const net of nets[name] ?? []) {
          console.log(indent(net.address, 4));
        }
      }
    })
    .bindLifecycle()
    .promise();
}

main().catch(console.error);
