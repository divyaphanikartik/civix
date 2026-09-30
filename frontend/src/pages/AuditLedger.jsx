import React from "react";
import PageContainer from "../components/layout/PageContainer";
import { useHotspots } from "../hooks/useHotspots";

export default function AuditLedger() {
  const {
    hotspots,
    loading,
    error,
  } = useHotspots();

  return (
    <PageContainer
      title="Audit Ledger"
      subtitle="Transparent record of the inputs used to calculate hotspot priority"
      fullWidth
    >
      {loading && (
        <div className="loading-state">
          Loading audit records...
        </div>
      )}

      {error && (
        <div className="error-state">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="table-container">
          <table className="audit-table">
            <thead>
              <tr>
                <th>Hotspot</th>
                <th>Sector</th>
                <th>Complaints</th>
                <th>MPI</th>
                <th>Distance km</th>
                <th>Budget ₹L</th>
                <th>Demand / 30</th>
                <th>Equity / 30</th>
                <th>Deficit / 25</th>
                <th>Budget / 15</th>
                <th>Total</th>
              </tr>
            </thead>

            <tbody>
              {hotspots.map((hotspot) => (
                <tr key={hotspot.id}>
                  <td>
                    <strong>
                      {hotspot.hotspot_code}
                    </strong>
                  </td>

                  <td>{hotspot.sector}</td>

                  <td>
                    {hotspot.complaints ?? 0}
                  </td>

                  <td>
                    {Number(
                      hotspot.mpi ?? 0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.distance_to_facility_km ??
                        0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.budget_lakhs ?? 0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.demand_score ?? 0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.equity_score ?? 0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.deficit_score ?? 0
                    ).toFixed(2)}
                  </td>

                  <td>
                    {Number(
                      hotspot.budget_score ?? 0
                    ).toFixed(2)}
                  </td>

                  <td className="score-cell">
                    {Number(
                      hotspot.total_score ?? 0
                    ).toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </PageContainer>
  );
}