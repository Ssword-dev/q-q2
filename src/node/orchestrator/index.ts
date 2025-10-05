import AppInstance from "./implementation";
import { App } from "./types";

/**
 * @returns an application.
 */
function app(): App {
  return new AppInstance() as unknown as App;
}

export default app;
export type { App };
export type * from "./types";
