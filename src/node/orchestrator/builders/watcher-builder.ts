// chokidar
import { FSWatcher, watch as createWatcher, FSWatcherEventMap } from "chokidar";
import Builder from "./base";
import { AppBase } from "../types";

// http

// sub-processing

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
class WatcherBuilder<O extends AppBase> extends Builder<O> {
  _watcher: FSWatcher | null;

  constructor(
    owner: O,
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
    this._watcher = null;
    super.finalize();
    return owner;
  }
}

export default WatcherBuilder;
