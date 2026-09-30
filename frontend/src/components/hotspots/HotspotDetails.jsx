import ScoreBreakdown
  from "./ScoreBreakdown";


export default function HotspotDetails({
  hotspot
}) {

  return (

    <div>

      <h2>
        {hotspot.panchayat}
      </h2>

      <p>
        {hotspot.dominant_issue}
      </p>


      <div className="metrics">

        <div>
          <strong>
            {hotspot.total_score}
          </strong>

          <span>
            Priority Score
          </span>
        </div>


        <div>
          <strong>
            {hotspot.complaints}
          </strong>

          <span>
            Complaints
          </span>
        </div>


        <div>
          <strong>
            {hotspot.mpi_score}
          </strong>

          <span>
            MPI
          </span>
        </div>

      </div>


      <ScoreBreakdown
        hotspot={hotspot}
      />

    </div>

  );
}