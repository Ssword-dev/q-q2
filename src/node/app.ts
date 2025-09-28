import express from 'express';

// proxy + caching
import {
  createProxyMiddleware,
  proxyEventsPlugin,
  Options as HTTPProxyMiddlewareOptions,
} from 'http-proxy-middleware';

import { LRUCache as LRU } from 'lru-cache';

// vite
import {
  createServer as createViteServer,
  InlineConfig,
  ResolvedConfig,
} from 'vite';

// chokidar
import { FSWatcher, watch as createWatcher, FSWatcherEventMap } from 'chokidar';

// http
import { Server } from 'node:http';

// sub-processing
import {
  spawn,
  ChildProcess,
  SpawnOptionsWithoutStdio,
  SpawnOptions,
  exec,
} from 'node:child_process';
import EventEmitter from 'node:events';
import { Service } from './service';
import { ApplicationRequestHandler } from 'express-serve-static-core';
import { ForwardMethod, GenericMethod } from './types';

/**
 * The Builder base class, provides common methods for all
 * builder subclasses.
 */
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

/**
 * # WatcherBuilder
 *
 * A WatcherBuilder is a description of a ***Filesystem Watcher***.
 *
 * ## Purpose
 *
 * The purpose of a WatcherBuilder is to provide a fluent API to configure
 * individual ***watchers**.
 *
 * ## Finalization
 *
 * The builder must be ***finalized*** for the builder to take effect.
 *
 * Note that after finalization, the builder will dispose the reference
 * to the owner and the corresponding builder result reference is released.
 *
 * ## Termination
 *
 * The watcher will be **terminated** at the **disposal** of the ***owner application.***
 */
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
      throw new Error('Cannot refinalize finalized builder.');
    }

    owner._watchers.push(this._watcher);
    this._watcher = null;
    super.finalize();
    return owner;
  }
}

/**
 * # ProcessBuilder
 *
 * A ProcessBuilder is a description of a ***Process***.
 *
 * ## Purpose
 *
 * The purpose of a ProcessBuilder is to provide a fluent API to configure
 * individual ***Process**.
 *
 * ## Finalization
 *
 * The builder must be ***finalized*** for the builder to take effect.
 *
 * Note that after finalization, the builder will dispose the reference
 * to the owner and the corresponding builder result reference is released.
 *
 * ## Termination
 *
 * The process will be **terminated** at the **disposal** of the ***owner application.***
 */
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

/**
 * # ServiceBuilder
 *
 * A ServiceBuilder is a description of a ***Service***.
 *
 * ## Purpose
 *
 * The purpose of a WatcherBuilder is to provide a fluent API to configure
 * individual ***services**.
 *
 * ## Finalization
 *
 * The builder must be ***finalized*** for the builder to take effect.
 *
 * Note that after finalization, the builder will dispose the reference
 * to the owner and the corresponding builder result reference is released.
 *
 * ## Termination
 *
 * The service will be **terminated** at the **disposal** of the ***owner application.***
 */
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
    });
    return super.finalize();
  }
}

/**
 * # App
 *
 * An app is a wrapper of `express.Express` that may or may
 * not define behaviours depending on the current environment.
 *
 * ## Purpose
 *
 * An app is a special entity that orchestrates common CL features
 * such as servers, subprocesses, services, and more.
 *
 * ## Sequential Initiation
 *
 * App initiation is ***sequential*** by design, the app uses
 * a linked-list style of execution by chaining ***promises***
 * via the `_last_promise_1` internal property.
 *
 * ## Subprocess, Service, and Watcher Termination.
 *
 * Any ***subprocess*** started via the API method `addSubprocess`,
 * any ***service*** started via the API method `addService`,
 * and any ***watcher*** started via the API method `addWatcher`
 * will be killed **before** the app's termination.
 *
 * ## Builders
 *
 * Any ***builder*** object generated by API methods must be finalized to
 * take effect.
 */
class App extends EventEmitter {
  private _express: express.Express;
  private _server: Server | null;
  public _watchers: FSWatcher[];
  public _sub_processes: ChildProcess[];
  public _services: Service[];
  private _last_promise_1: Promise<any> | null;
  /**
   * @inheritdoc
   */
  constructor() {
    super();
    this._express = express();
    this._watchers = [];
    this._sub_processes = [];
    this._services = [];
    this._server = null;
    this._last_promise_1 = null;
  }

  listen(...args: any[]) {
    this.enterCritical(async () => {
      this._server = this._express.listen(...args);
    });

    return this;
  }

  async dispose() {
    if (!this._server) {
      throw new Error('Please call .listen before .dispose!');
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
      sp.kill('SIGTERM');
    }

    for (const s of this._services) {
      await s.dispose();
      console.log(`Disposed ${s.name}`);
    }

    process.exit(0);
  }

  /**
   * @param route The route to take proxy request from.
   * @param options The options for the proxy.
   * @returns everything returns this or a builder. except dispose.
   * or other future methods.
   */
  addProxy(route: string, options: HTTPProxyMiddlewareOptions) {
    this._express.use(route, createProxyMiddleware(options));
    return this;
  }

  /**
   * @param paths The paths of files and folders to watch.
   * @param options The options for the watcher.
   * @returns a watcher builder that can be used for configuring
   * the watcher further.
   */
  addWatcher(
    paths: string | string[],
    options: Parameters<typeof createWatcher>[1]
  ) {
    return new WatcherBuilder(this, paths, options);
  }

  /**
   * @param service The name of the service.
   * @returns a service builder that can be used for configuring
   * the service.
   */
  addService(service: string) {
    return new ServiceBuilder(this, service);
  }

  /**
   * @param executable The command /path to the executable, preferably
   * absolute paths.
   * @param args The argument values, or argv in C / C++ and other languages.
   * @returns A subprocess builder that can be used to configure the subprocess further.
   */
  addSubprocess(executable: string, args: string[]) {
    return new ProcessBuilder(this, executable, args);
  }

  /**
   * @param opts The options for vite.
   * @returns also returns `this`.
   */
  addVite(opts: Partial<Omit<InlineConfig & ResolvedConfig, 'server'>>) {
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

  /**
   * @param cb Action to run when development.
   * @returns also returns `this`.
   */
  ifDev(cb: (app: App) => void) {
    if (process.env.NODE_ENV === 'development') {
      cb(this);
    }
    return this;
  }

  /**
   * @param cb Action to run on production.
   * @returns also returns `this`.
   */
  ifProd(cb: (app: App) => void) {
    if (process.env.NODE_ENV === 'production') {
      cb(this);
    }

    return this;
  }

  /**
   * @param cb Functin to apply to app.
   * @returns also returns `this`.
   */
  apply(cb: (app: App) => void) {
    cb(this);
    return this;
  }

  /**
   * Binds the lifecycle of the app to actual process lifecycle.
   * @returns also returns this.
   */
  bindLifecycle() {
    const arrow = this.dispose.bind(this);

    process.on('SIGINT', arrow).on('SIGTERM', arrow);
    return this;
  }

  /**
   * An internal method for entering asyncronous operations.
   * @param cb async callback to run sequentially.
   */
  public enterCritical(cb: () => Promise<any>) {
    if (this._last_promise_1) {
      this._last_promise_1.then(() => (this._last_promise_1 = cb()));
    } else {
      this._last_promise_1 = cb();
    }
  }

  /**
   * @returns The last promise or a resolved null promise.
   */
  async promise() {
    return this._last_promise_1 ? this._last_promise_1 : Promise.resolve(null);
  }

  // forward calls.
  public use(route: string, ...handlers: express.RequestHandler[]) {
    this._express.use(route, ...handlers);
    return this;
  }

  public get(route: string, ...handlers: express.RequestHandler[]) {
    this._express.get(route, ...handlers);
    return this;
  }

  public put(route: string, ...handlers: express.RequestHandler[]) {
    this._express.put(route, ...handlers);
    return this;
  }

  public post(route: string, ...handlers: express.RequestHandler[]) {
    this._express.post(route, ...handlers);
    return this;
  }

  public delete(route: string, ...handlers: express.RequestHandler[]) {
    this._express.delete(route, ...handlers);
    return this;
  }

  public patch(route: string, ...handlers: express.RequestHandler[]) {
    this._express.patch(route, ...handlers);
    return this;
  }

  public options(route: string, ...handlers: express.RequestHandler[]) {
    this._express.options(route, ...handlers);
    return this;
  }

  public head(route: string, ...handlers: express.RequestHandler[]) {
    this._express.head(route, ...handlers);
    return this;
  }
}

/**
 * @returns
 */
function app() {
  return new App();
}

export default app;
export type { App };
