import express from "express";

// types for express packages.
import type * as ServeProxy from "http-proxy-middleware";

import type * as ServeStatic from "serve-static";
// vite
import type * as Vite from "vite";

// chokidar
import { FSWatcher, watch as createWatcher } from "chokidar";

// http
import { Server } from "node:http";

// sub-processing
import { ChildProcess } from "node:child_process";
import Service from "./service";
import ProcessBuilder from "./builders/process-builder";
import ServiceBuilder from "./builders/service-builder";
import WatcherBuilder from "./builders/watcher-builder";

type Applyable<T> = (...args: [T]) => void;

/**
 * Core instance of App.
 */
interface AppBase {
  // lifecycle
  listen(...args: any[]): this;
  dispose(): Promise<void>;
  bindLifecycle(): this;

  // integrations
  proxy(route: string, options: ServeProxy.Options): this;
  static(
    route: string,
    root: string,
    options?: ServeStatic.ServeStaticOptions
  ): this;
  addWatcher<T extends AppBase>(
    this: T,
    paths: string | string[],
    options: Parameters<typeof createWatcher>[1]
  ): WatcherBuilder<T>;
  addService<T extends AppBase>(this: T, service: string): ServiceBuilder<this>;
  addSubprocess<T extends AppBase>(
    this: T,
    executable: string,
    args: string[]
  ): ProcessBuilder<T>;
  addVite(
    opts: Partial<Omit<Vite.InlineConfig & Vite.ResolvedConfig, "server">>
  ): this;

  // environment utilities
  ifDev(cb: (app: this) => void): this;
  ifProd(cb: (app: this) => void): this;
  apply(cb: (app: this) => void): this;

  // async control
  enterCritical(cb: () => Promise<any>): void;
  promise(): Promise<any | null>;

  readonly _watchers: FSWatcher[];
  readonly _sub_processes: ChildProcess[];
  readonly _services: Service[];
  readonly _server: Server | null;
}

interface App extends AppBase {
  // upgrades.
  express<T extends App>(this: T): AppWithExpress<T>;
}

interface ExpressHandle {
  _express: express.Express;
}

interface ExpressForwardMethods {
  use(route: string, ...handlers: express.RequestHandler[]): this;
  get(route: string, ...handlers: express.RequestHandler[]): this;
  put(route: string, ...handlers: express.RequestHandler[]): this;
  post(route: string, ...handlers: express.RequestHandler[]): this;
  delete(route: string, ...handlers: express.RequestHandler[]): this;
  patch(route: string, ...handlers: express.RequestHandler[]): this;
  options(route: string, ...handlers: express.RequestHandler[]): this;
  head(route: string, ...handlers: express.RequestHandler[]): this;
}

interface _AppWithExpress
  extends Omit<App, "express">,
    ExpressHandle,
    ExpressForwardMethods {}

type AppWithExpress<T extends App> = _AppWithExpress &
  Omit<T, keyof _AppWithExpress>;

export type {
  App,
  AppBase,
  AppWithExpress,
  Applyable,
  ExpressForwardMethods,
  ExpressHandle,
  _AppWithExpress as __INTERNAL_APP_WITH_EXPRESS_INTERFACE_DO_NOT_TOUCH,
};
