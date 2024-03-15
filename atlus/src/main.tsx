import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { NextUIProvider } from "@nextui-org/react";
import Navbar from "./components/Navbar.tsx";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <NextUIProvider>
      <main
        className="dark text-foreground bg-background"
        style={{ minHeight: "100vh" }}
      >
        <Navbar />
        <App />
      </main>
    </NextUIProvider>
  </React.StrictMode>
);
