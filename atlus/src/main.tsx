import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { NextUIProvider } from "@nextui-org/react";
import Navbar from "./components/Navbar.tsx";

function isDarkModeEnabled(): boolean {
  if (window.matchMedia) {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  return false;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <NextUIProvider
      className={`${
        isDarkModeEnabled() ? "dark" : "light"
      } text-foreground bg-background`}
    >
      <Navbar />
      <App />
    </NextUIProvider>
  </React.StrictMode>
);
