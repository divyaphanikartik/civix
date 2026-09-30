import React from "react";
import Header from "./Header";

export default function PageContainer({
  children,
  title,
  subtitle,
  fullWidth = false,
}) {
  return (
    <main className={`page-container ${fullWidth ? "page-full-width" : ""}`}>
      <Header title={title} />

      {subtitle && (
        <p className="page-subtitle">
          {subtitle}
        </p>
      )}

      <section className="page-content">
        {children}
      </section>
    </main>
  );
}