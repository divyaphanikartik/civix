export default function ProjectConceptNote({
  project
}) {

  if (!project) {
    return null;
  }


  return (

    <article>

      <h1>
        {project.project_title}
      </h1>


      <p>
        <strong>
          Funding Scheme:
        </strong>

        {" "}

        {project.recommended_central_scheme}
      </p>


      <p>
        <strong>
          Estimated Outlay:
        </strong>

        {" "}

        ₹
        {project.estimated_capital_outlay_inr_lakhs}
        Lakh
      </p>


      <p>
        <strong>
          Beneficiaries:
        </strong>

        {" "}

        {project.estimated_beneficiaries}
      </p>


      <h2>
        Problem Statement
      </h2>

      <p>
        {project.executive_problem_statement}
      </p>


      <h2>
        Socio-Economic Impact
      </h2>

      <p>
        {project.socio_economic_impact_justification}
      </p>


      <h2>
        Risks & Feasibility
      </h2>

      <ul>

        {project.risk_and_feasibility_flags.map(
          (risk, index) => (

            <li key={index}>
              {risk}
            </li>

          )
        )}

      </ul>

    </article>

  );
}