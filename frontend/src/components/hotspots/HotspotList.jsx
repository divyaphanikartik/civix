import HotspotCard
  from "./HotspotCard";


export default function HotspotList({
  hotspots
}) {

  return (

    <div>

      <h2>
        Priority Hotspots
      </h2>


      {hotspots.map(
        hotspot => (

          <HotspotCard
            key={hotspot.id}
            hotspot={hotspot}
          />

        )
      )}

    </div>

  );
}