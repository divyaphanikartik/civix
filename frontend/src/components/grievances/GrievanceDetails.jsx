import React from "react";
import ProcessingStatus from "./ProcessingStatus";

export default function GrievanceDetails({ grievance }) {
  if (!grievance) {
    return (
      <div className="empty-state">
        Select a grievance to view details.
      </div>
    );
  }

  return (
    <div className="grievance-details">
      <div className="detail-card">
        <div className="detail-card-header">
          <div>
            <h2>Grievance Details</h2>
            <span className="muted">
              ID: {grievance.id}
            </span>
          </div>

          <span
            className={`urgency-badge urgency-${String(
              grievance.urgency || "low"
            ).toLowerCase()}`}
          >
            {grievance.urgency || "Unknown"}
          </span>
        </div>

        <ProcessingStatus status={grievance.status} />
      </div>

      <div className="detail-grid">
        <div className="detail-card">
          <h3>Classification</h3>

          <DetailRow
            label="Sector"
            value={grievance.sector}
          />

          <DetailRow
            label="Asset Type"
            value={grievance.asset_type}
          />

          <DetailRow
            label="Failure Mode"
            value={grievance.failure_mode}
          />

          <DetailRow
            label="Language"
            value={grievance.detected_language}
          />
        </div>

        <div className="detail-card">
          <h3>Location</h3>

          <DetailRow
            label="Reported Location"
            value={grievance.reported_location_name}
          />

          <DetailRow
            label="Incident Latitude"
            value={grievance.incident_latitude}
          />

          <DetailRow
            label="Incident Longitude"
            value={grievance.incident_longitude}
          />

          <DetailRow
            label="Reporter Latitude"
            value={grievance.reporter_latitude}
          />

          <DetailRow
            label="Reporter Longitude"
            value={grievance.reporter_longitude}
          />
        </div>
      </div>

      <div className="detail-card">
        <h3>English Translation</h3>

        <p className="translation-text">
          {grievance.english_translation ||
            "Translation not available."}
        </p>
      </div>

      <div className="detail-card">
        <h3>Visual Evidence</h3>

        <p>
          {grievance.visual_evidence_analysis ||
            "No visual evidence analysis available."}
        </p>
      </div>

      <div className="detail-card">
        <h3>Confidence</h3>

        <div className="confidence-bar">
          <div
            className="confidence-fill"
            style={{
              width: `${Math.max(
                0,
                Math.min(
                  100,
                  (grievance.confidence_score || 0) * 100
                )
              )}%`,
            }}
          />
        </div>

        <div className="confidence-value">
          {(
            (grievance.confidence_score || 0) * 100
          ).toFixed(1)}
          %
        </div>
      </div>
    </div>
  );
}

function DetailRow({ label, value }) {
  return (
    <div className="detail-row">
      <span className="detail-label">{label}</span>
      <span className="detail-value">
        {value ?? "—"}
      </span>
    </div>
  );
}