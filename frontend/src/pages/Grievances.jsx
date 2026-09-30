import {
  useEffect,
  useState
} from "react";

import {
  getGrievances
} from "../services/api";


export default function Grievances() {

  const [grievances, setGrievances] =
    useState([]);


  useEffect(() => {

    getGrievances()
      .then(setGrievances)
      .catch(console.error);

  }, []);


  return (

    <div>

      <h1>
        Citizen Grievances
      </h1>


      {grievances.map(
        grievance => (

          <div
            key={grievance.id}
          >

            <strong>
              {grievance.sector}
            </strong>

            <p>
              {grievance.english_translation}
            </p>

            <small>
              Status:
              {" "}
              {grievance.status}
            </small>

          </div>

        )
      )}

    </div>

  );
}