import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

interface LoaderOptions {
  esModuleInterop?: boolean;
}

interface Lazy<T> {
  readonly value: T;
}

const UNCOMPUTED_LAZY_VALUE = Symbol("uncomputed");

// helper to test if a node js feature is supported
// without crashing the whole app.
const isSupported = (fn: () => boolean) => {
  try {
    return fn();
  } catch (_) {
    return false;
  }
};

const importMetaResolveIsSupported = isSupported(
  () => typeof import.meta.resolve === "function"
);

const defaultLoaderOptions: LoaderOptions = {
  esModuleInterop: true,
};

function createLoader(
  base: string,
  options: LoaderOptions = defaultLoaderOptions
) {
  // cjs require.
  const require = createRequire(base);

  // create a null prototyped cache to avoid issues with __proto__.
  const cache = Object.create(null);

  const resolve = async (id: string) => {
    const errors = [];
    if (importMetaResolveIsSupported) {
      try {
        return {
          type: "esm",
          path: import.meta.resolve(id, pathToFileURL(base).href),
        } as const;
      } catch (esmError) {
        errors.push(esmError);
      } // ignore
    }

    try {
      return { type: "cjs", path: require.resolve(id) } as const;
    } catch (cjsError) {
      errors.push(cjsError);
    }

    throw new AggregateError(errors, `Failed to resolve module '${id}'.`);
  };

  // loader.
  const lazyImport = async function <T>(id: string): Promise<T> {
    const cachedImplicitModule = cache[id];
    if (typeof cachedImplicitModule !== "undefined") {
      return cachedImplicitModule;
    }

    const { type, path } = await resolve(id);
    const cacheExplicitModule = cache[path];

    if (typeof cacheExplicitModule !== "undefined") {
      return cacheExplicitModule;
    }

    let exports = type === "esm" ? await import(path) : require(path);

    // interop with babel style "esm" cjs.
    if ("default" in exports && exports.__esModule && options.esModuleInterop) {
      exports = exports.default;
    }

    cache[id] = exports;
    cache[path] = exports;
    return exports;
  };

  return lazyImport;
}

function makeLazy<T>(fn: () => T): Lazy<T> {
  // as a unique symbol so no collision when value is falsy.
  let lazilyComputedValue: any = UNCOMPUTED_LAZY_VALUE;

  const lazy = {
    get value() {
      if (lazilyComputedValue === UNCOMPUTED_LAZY_VALUE) {
        lazilyComputedValue = fn();
      }

      return lazilyComputedValue;
    },
  };

  return lazy;
}

function createLazyLoader(
  base: string,
  options: LoaderOptions = defaultLoaderOptions
) {
  const baseLoader = createLoader(base, options);
  return function <T>(id: string) {
    return makeLazy<Promise<T>>(async () => await baseLoader(id));
  };
}

export { createLoader, createLazyLoader };
