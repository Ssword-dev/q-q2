import Holidays from "date-holidays";
import express from "express";
import { App, AppWithExpress } from "./orchestrator";

function formatDate(d: Date) {
  const month = d.getMonth() + 1; // getMonth returns 0 for january, ..., so need + 1 because off by one.
  const day = d.getDate(); // weirdly, this does not start with 0.
  return `${d.getFullYear()}-${month > 9 ? month : `0${month}`}-${day > 9 ? day : `0${day}`}`; // as YY-MM-DD format.
}

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
  const response = holidayMappings;

  res.json(response);
}

function routes(app: AppWithExpress<App>) {
  app.get(
    "/api/node/holidays/:year/:country",
    // decay the type down to an ordinary request handler
    handleHolidaysRoute as unknown as express.RequestHandler
  );
}

export default routes;
