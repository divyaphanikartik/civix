export default function HotspotCard({
  hotspot
}) {

  return (

    <div className="hotspot-card">

      <h3>
        {hotspot.panchayat}
      </h3>

      <p>
        {hotspot.district},
        {" "}
        {hotspot.state}
      </p>

      <p>
        {hotspot.sector}
      </p>

      <strong>
        Priority Score:
        {" "}
        {hotspot.total_score}
        /100
      </strong>

    </div>

  );
}