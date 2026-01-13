import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { HeroUIProvider } from "@heroui/react";
import Navbar from "./components/Navbar.tsx";

function isDarkModeEnabled(): boolean {
  if (window.matchMedia) {
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  return false;
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <HeroUIProvider
    className={`${
      isDarkModeEnabled() ? "dark" : "light"
    } text-foreground bg-background`}
  >
    <Navbar />
    <App dark={isDarkModeEnabled()} />
  </HeroUIProvider>,
);
