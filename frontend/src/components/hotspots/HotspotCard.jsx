export default function HotspotCard({ hotspot }) {
  const location = [
    hotspot.panchayat,
    hotspot.block,
    hotspot.district,
    hotspot.state,
  ]
    .filter(Boolean)
    .join(", ");

  return (
    <div className="hotspot-card">
      <div className="hotspot-card-topline">
        <span className="hotspot-code">{hotspot.hotspot_code}</span>
        <span className="hotspot-status">{hotspot.status || "ACTIVE"}</span>
      </div>

      <h3>{location || "Location not specified"}</h3>

      <p>{hotspot.sector}</p>

      <p className="hotspot-issue">
        {hotspot.dominant_issue || "Issue not specified"}
      </p>

      <div className="hotspot-card-metrics">
        <div>
          <strong>{Number(hotspot.total_score || 0).toFixed(2)}</strong>
          <span>Priority /100</span>
        </div>
        <div>
          <strong>{hotspot.complaints || 0}</strong>
          <span>Complaints</span>
        </div>
        <div>
          <strong>{Number(hotspot.mpi_score || 0).toFixed(2)}</strong>
          <span>MPI</span>
        </div>
      </div>
    </div>
  );
}
