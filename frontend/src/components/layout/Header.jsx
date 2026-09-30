import React from "react";

export default function Header({ title = "Dashboard" }) {
  return (
    <header className="civix-header">
      <div>
        <h1>{title}</h1>
        <p className="header-subtitle">
          Citizen-driven infrastructure intelligence
        </p>
      </div>

      <div className="header-status">
        <span className="status-dot" />
        <span>System Operational</span>
      </div>
    </header>
  );
}