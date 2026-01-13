import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  const base = command === "serve" ? "/" : "/atlus_website/";

  return {
    server: {
      host: true,
      port: 5173,
      watch: {
        usePolling: true,
      },
    },
    plugins: [react(), tailwindcss()],
    base,
    build: {
      rollupOptions: {
        output: {
          manualChunks: undefined,
        },
      },
    },
    optimizeDeps: {
      include: [
        "@heroui/react",
        "@heroui/theme",
        "@heroui/dom-animation",
        "framer-motion",
      ],
    },
  };
});
