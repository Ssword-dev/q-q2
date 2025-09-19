import express from "express";
import {
  createProxyMiddleware,
  Options as HTTPProxyMiddlewareOptions,
} from "http-proxy-middleware";

// vite
import {
  createServer as createViteServer,
  InlineConfig,
  ResolvedConfig,
} from "vite";

// chokidar
import { FSWatcher, watch as createWatcher, FSWatcherEventMap } from "chokidar";

// http
import { Server } from "node:http";

// sub-processing
import {
  spawn,
  ChildProcess,
  SpawnOptionsWithoutStdio,
  SpawnOptions,
  exec,
} from "node:child_process";
import EventEmitter from "node:events";
import { Service } from "./service";

Service;

class Builder {
  owner: App | null;
  constructor(owner: App) {
    this.owner = owner;
  }

  /**
   * Finalizes the builder and returns the owner.
   */
  finalize() {
    const owner = this.owner;
    this.owner = null;
    return owner!;
  }
}

class WatcherBuilder extends Builder {
  _watcher: FSWatcher | null;

  constructor(
    owner: App,
    paths: string | string[],
    options: Parameters<typeof createWatcher>[1]
  ) {
    super(owner);
    this._watcher = createWatcher(paths, options);
  }

  addListener<K extends keyof FSWatcherEventMap>(
    type: K,
    handler: (...args: FSWatcherEventMap[K]) => void
  ) {
    this._watcher!.addListener<K>(type, handler as any);
    return this;
  }

  finalize() {
    const owner = this.owner;

    if (!owner || !this._watcher) {
      throw new Error("Cannot refinalize finalized builder.");
    }

    owner._watchers.push(this._watcher);
    super.finalize();
    return owner;
  }
}

class ProcessBuilder extends Builder {
  _executable: string;
  _args: string[];
  _options: SpawnOptions;

  constructor(owner: App, executable: string, args: string[]) {
    super(owner);
    this._executable = executable;
    this._args = args;
    this._options = {};
  }

  addOption<O extends keyof SpawnOptionsWithoutStdio>(
    opt: O,
    value: SpawnOptionsWithoutStdio[O]
  ) {
    this._options[opt] = value;
    return this;
  }

  finalize() {
    this.owner?._sub_processes.push(
      spawn(this._executable, this._args, this._options)
    );

    return super.finalize();
  }
}

class ServiceBuilder extends Builder {
  _service: string;

  constructor(owner: App, service: string) {
    super(owner);
    this._service = service;
  }

  finalize() {
    const owner = this.owner!;
    owner.enterCritical(async () => {
      const service = new Service(this._service);
      owner._services.push(service);
      await service.start();
      console.log(`Started service...`);
    });
    return super.finalize();
  }
}

class App {
  private _express: express.Express;
  private _server: Server | null;
  public _watchers: FSWatcher[];
  public _sub_processes: ChildProcess[];
  public _services: Service[];
  private _last_promise_1: Promise<any> | null;

  constructor() {
    this._express = express();
    this._watchers = [];
    this._sub_processes = [];
    this._services = [];
    this._server = null;
    this._last_promise_1 = null;
  }

  listen(...args: Parameters<express.Express["listen"]>) {
    this.enterCritical(async () => {
      this._server = this._express.listen(...args);
    });

    return this;
  }

  async dispose() {
    if (!this._server) {
      throw new Error("Please call .listen before .dispose!");
    }

    await new Promise<void>((resolve, reject) => {
      if (!this._server) return resolve();
      this._server.close((err) => (err ? reject(err) : resolve()));
    });

    for (const w of this._watchers) {
      await w.close();
    }

    for (const sp of this._sub_processes) {
      if (sp.killed) continue;
      sp.kill("SIGTERM");
    }

    for (const s of this._services) {
      await s.dispose();
      console.log(`Disposed ${s.name}`);
    }
  }

  addProxy(route: string, options: HTTPProxyMiddlewareOptions) {
    this._express.use(route, createProxyMiddleware(options));
    return this;
  }

  addWatcher(
    paths: string | string[],
    options: Parameters<typeof createWatcher>[1]
  ) {
    return new WatcherBuilder(this, paths, options);
  }

  addService(service: string) {
    return new ServiceBuilder(this, service);
  }

  addSubprocess(executable: string, args: string[]) {
    return new ProcessBuilder(this, executable, args);
  }

  addVite(opts: Partial<Omit<InlineConfig & ResolvedConfig, "server">>) {
    const vite_promise = createViteServer({
      ...opts,
      server: {
        middlewareMode: true,
      },
    });

    this.enterCritical(async () => {
      const vite = await vite_promise;
      vite.bindCLIShortcuts();
      this._express.use(vite.middlewares);
    });

    return this;
  }

  // utilities

  ifDev(cb: (app: App) => void) {
    if (process.env.NODE_ENV === "development") {
      cb(this);
    }
    return this;
  }

  ifNotDev(cb: (app: App) => void) {
    if (process.env.NODE_ENV === "production") {
      cb(this);
    }

    return this;
  }

  use(cb: (app: App) => void) {
    cb(this);
    return this;
  }

  bindLifecycle() {
    const arrow = this.dispose.bind(this);

    process.on("beforeExit", arrow).on("SIGINT", arrow).on("SIGTERM", arrow);
  }

  public enterCritical(cb: () => Promise<any>) {
    if (this._last_promise_1) {
      this._last_promise_1.then(() => (this._last_promise_1 = cb()));
    } else {
      this._last_promise_1 = cb();
    }
  }

  async promise() {
    return this._last_promise_1 ? this._last_promise_1 : Promise.resolve();
  }
}

function app() {
  return new App();
}

export default app;
