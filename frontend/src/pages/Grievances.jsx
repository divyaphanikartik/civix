import React from "react";
import PageContainer from "../components/layout/PageContainer";
import { useGrievances } from "../hooks/useGrievances";

export default function Grievances() {
  const {
    grievances,
    loading,
    error,
    refresh,
  } = useGrievances();

  return (
    <PageContainer
      title="Citizen Grievances"
      subtitle="Citizen-reported infrastructure issues received through Civix"
    >
      {loading && (
        <div className="loading-state">
          Loading grievances...
        </div>
      )}

      {error && (
        <div className="error-state">
          <strong>Unable to load grievances</strong>
          <p>{error}</p>

          <button
            className="primary-button"
            onClick={refresh}
          >
            Retry
          </button>
        </div>
      )}

      {!loading &&
        !error &&
        grievances.length === 0 && (
          <div className="empty-state">
            <h3>No grievances received yet</h3>
            <p>
              Citizen grievances received through
              WhatsApp will appear here after processing.
            </p>
          </div>
        )}

      {!loading &&
        !error &&
        grievances.length > 0 && (
          <div className="grievance-list">
            {grievances.map((grievance) => (
              <article
                className="detail-card"
                key={grievance.id}
              >
                <div className="grievance-header">
                  <div>
                    <h3>
                      Grievance #{grievance.id}
                    </h3>

                    <span className="grievance-sector">
                      {grievance.sector ||
                        "Unclassified"}
                    </span>
                  </div>

                  <span className="status-badge">
                    {grievance.status ||
                      "RECEIVED"}
                  </span>
                </div>

                <p>
                  {grievance.english_translation ||
                    "No translation available"}
                </p>

                <div className="detail-grid">
                  <div>
                    <strong>Language</strong>
                    <div>
                      {grievance.detected_language ||
                        "—"}
                    </div>
                  </div>

                  <div>
                    <strong>Urgency</strong>
                    <div>
                      {grievance.urgency || "—"}
                    </div>
                  </div>

                  <div>
                    <strong>Asset</strong>
                    <div>
                      {grievance.asset_type || "—"}
                    </div>
                  </div>

                  <div>
                    <strong>Failure Mode</strong>
                    <div>
                      {grievance.failure_mode || "—"}
                    </div>
                  </div>

                  <div>
                    <strong>Reported Location</strong>
                    <div>
                      {grievance.reported_location_name ||
                        "—"}
                    </div>
                  </div>

                  <div>
                    <strong>Confidence</strong>
                    <div>
                      {grievance.confidence_score != null
                        ? `${(
                            Number(
                              grievance.confidence_score
                            ) * 100
                          ).toFixed(1)}%`
                        : "—"}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )}
    </PageContainer>
  );
}