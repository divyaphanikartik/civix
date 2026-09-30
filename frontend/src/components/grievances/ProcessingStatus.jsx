import React from "react";

const statuses = [
  "RECEIVED",
  "PROCESSING",
  "LOCATION RESOLVED",
  "SCORED",
  "HOTSPOT CREATED",
];

function normalizeStatus(status) {
  return (status || "").toUpperCase().replace(/_/g, " ");
}

export default function ProcessingStatus({ status }) {
  const currentStatus = normalizeStatus(status);

  const currentIndex = statuses.indexOf(currentStatus);

  return (
    <div className="processing-status">
      {statuses.map((item, index) => {
        const completed =
          currentIndex >= 0 && index <= currentIndex;

        const active = index === currentIndex;

        return (
          <div
            key={item}
            className={`processing-step ${
              completed ? "completed" : ""
            } ${active ? "active" : ""}`}
          >
            <div className="processing-dot">
              {completed ? "✓" : index + 1}
            </div>

            <div className="processing-label">
              {item}
            </div>

            {index < statuses.length - 1 && (
              <div
                className={`processing-line ${
                  currentIndex > index ? "completed" : ""
                }`}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}