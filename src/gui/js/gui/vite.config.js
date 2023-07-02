import { resolve } from "path";
import { defineConfig } from "vite";

// vite.config.js
export default {
  // config options
  build: {
    lib: {
      entry: resolve(__dirname, "main.js"),
      name: "testlib",
    },
    outDir: "../../static/gui",
  },
};
