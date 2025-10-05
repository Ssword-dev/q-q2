import { createLazyLoader } from "./loaders";

const lazyImport = createLazyLoader(import.meta.dirname, {
  esModuleInterop: true,
});

export default lazyImport;
