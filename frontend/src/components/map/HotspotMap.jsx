import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from "react-leaflet";

import "leaflet/dist/leaflet.css";


export default function HotspotMap({
  hotspots
}) {

  const center = [
    20.5937,
    78.9629
  ];


  return (

    <MapContainer
      center={center}
      zoom={5}
      style={{
        height: "600px",
        width: "100%"
      }}
    >

      <TileLayer
        attribution="OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />


      {hotspots.map(
        hotspot => (

          <Marker
            key={hotspot.id}
            position={[
              hotspot.latitude,
              hotspot.longitude
            ]}
          >

            <Popup>

              <strong>
                {hotspot.panchayat}
              </strong>

              <br />

              {hotspot.sector}

              <br />

              Priority:
              {" "}
              {hotspot.total_score}

            </Popup>

          </Marker>

        )
      )}

    </MapContainer>

  );
}