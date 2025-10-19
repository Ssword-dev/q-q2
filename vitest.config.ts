// was going to test. but later.

import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/app/*.tsx"],
  },
});
