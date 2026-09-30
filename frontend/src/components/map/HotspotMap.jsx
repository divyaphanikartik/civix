import { useEffect } from "react";
import {
  MapContainer,
  TileLayer,
  useMap,
} from "react-leaflet";

import HotspotMarker from "./HotspotMarker";
import "leaflet/dist/leaflet.css";

function FitHotspots({ hotspots }) {
  const map = useMap();

  useEffect(() => {
    const points = hotspots
      .filter(
        (hotspot) =>
          hotspot.latitude !== null &&
          hotspot.latitude !== undefined &&
          hotspot.longitude !== null &&
          hotspot.longitude !== undefined
      )
      .map((hotspot) => [hotspot.latitude, hotspot.longitude]);

    if (points.length === 1) {
      map.setView(points[0], 13);
    } else if (points.length > 1) {
      map.fitBounds(points, { padding: [40, 40] });
    }
  }, [hotspots, map]);

  return null;
}

export default function HotspotMap({ hotspots }) {
  const mappedHotspots = hotspots.filter(
    (hotspot) =>
      hotspot.latitude !== null &&
      hotspot.latitude !== undefined &&
      hotspot.longitude !== null &&
      hotspot.longitude !== undefined
  );

  return (
    <div className="hotspot-map-container">
      <div className="map-header">
        <div>
          <h2>Demand Hotspots</h2>
          <p>
            {mappedHotspots.length} of {hotspots.length} hotspots have mapped coordinates.
          </p>
        </div>
      </div>

      <MapContainer
        center={[20.5937, 78.9629]}
        zoom={5}
        style={{ height: "600px", width: "100%" }}
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <FitHotspots hotspots={mappedHotspots} />

        {mappedHotspots.map((hotspot) => (
          <HotspotMarker key={hotspot.id} hotspot={hotspot} />
        ))}
      </MapContainer>

      {hotspots.length > 0 && mappedHotspots.length === 0 && (
        <div className="map-empty-state">
          Hotspots are being recorded, but their incident location was not
          specified. Mention a locality or landmark in the WhatsApp complaint
          to place the hotspot on the map.
        </div>
      )}
    </div>
  );
}
