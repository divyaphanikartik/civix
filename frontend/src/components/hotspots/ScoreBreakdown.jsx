export default function ScoreBreakdown({
  hotspot
}) {

  return (

    <div>

      <h3>
        MCDA Score Breakdown
      </h3>


      <p>
        Demand:
        {" "}
        {hotspot.demand_score}
        /30
      </p>


      <p>
        Equity:
        {" "}
        {hotspot.equity_score}
        /30
      </p>


      <p>
        Deficit:
        {" "}
        {hotspot.deficit_score}
        /25
      </p>


      <p>
        Budget:
        {" "}
        {hotspot.budget_score}
        /15
      </p>

    </div>

  );
}