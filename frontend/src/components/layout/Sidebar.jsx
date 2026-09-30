import React from "react";
import { NavLink } from "react-router-dom";

const navigation = [
  {
    label: "Dashboard",
    path: "/",
  },
  {
    label: "Hotspots",
    path: "/hotspots",
  },
  {
    label: "Grievances",
    path: "/grievances",
  },
  {
    label: "Projects",
    path: "/projects",
  },
  {
    label: "Audit Ledger",
    path: "/audit",
  },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">C</div>

        <div>
          <div className="brand-name">Civix</div>
          <div className="brand-caption">Civic Intelligence</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navigation.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-title">
          WhatsApp Intake
        </div>

        <div className="sidebar-footer-status">
          <span className="status-dot" />
          Listening for grievances
        </div>
      </div>
    </aside>
  );
}