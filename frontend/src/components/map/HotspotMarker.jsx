import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

function getMarkerColor(score) {
  if (score >= 75) return "#dc2626";
  if (score >= 50) return "#f59e0b";
  return "#2563eb";
}

function createMarkerIcon(score) {
  const color = getMarkerColor(score);

  return L.divIcon({
    className: "civix-hotspot-marker",
    html: `
      <div
        style="
          width: 28px;
          height: 28px;
          border-radius: 50%;
          background: ${color};
          border: 3px solid white;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 10px;
          font-weight: 700;
        "
      >
        ${Math.round(score ?? 0)}
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -14],
  });
}

export default function HotspotMarker({ hotspot }) {
  if (
    hotspot.latitude === null ||
    hotspot.latitude === undefined ||
    hotspot.longitude === null ||
    hotspot.longitude === undefined
  ) {
    return null;
  }

  const score = hotspot.total_score ?? 0;

  return (
    <Marker
      position={[hotspot.latitude, hotspot.longitude]}
      icon={createMarkerIcon(score)}
    >
      <Popup>
        <div className="map-popup">
          <strong>{hotspot.hotspot_code}</strong>

          <div>
            {hotspot.panchayat || hotspot.target_administrative_unit}
          </div>

          <div>
            {hotspot.district}, {hotspot.state}
          </div>

          <hr />

          <div>
            <strong>Sector:</strong> {hotspot.sector}
          </div>

          <div>
            <strong>Issue:</strong>{" "}
            {hotspot.dominant_issue || "Not specified"}
          </div>

          <div>
            <strong>Priority:</strong>{" "}
            {Number(score).toFixed(2)}
          </div>
        </div>
      </Popup>
    </Marker>
  );
}