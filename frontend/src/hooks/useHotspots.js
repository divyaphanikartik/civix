import {
  useEffect,
  useState
} from "react";

import {
  getHotspots
} from "../services/api";


export function useHotspots() {

  const [hotspots, setHotspots] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);


  useEffect(() => {

    async function load() {

      try {

        const data =
          await getHotspots();

        setHotspots(data);

      } catch (err) {

        setError(err);

      } finally {

        setLoading(false);

      }

    }

    load();

  }, []);


  return {
    hotspots,
    loading,
    error
  };
}