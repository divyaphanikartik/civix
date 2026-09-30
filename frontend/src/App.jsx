import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Sidebar from "./components/layout/Sidebar";

import Dashboard from "./pages/Dashboard";
import Hotspots from "./pages/Hotspots";
import Grievances from "./pages/Grievances";
import Projects from "./pages/Projects";
import AuditLedger from "./pages/AuditLedger";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />

        <div className="main-content">
          <Routes>
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/hotspots"
              element={<Hotspots />}
            />

            <Route
              path="/grievances"
              element={<Grievances />}
            />

            <Route
              path="/projects"
              element={<Projects />}
            />

            <Route
              path="/audit"
              element={<AuditLedger />}
            />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}