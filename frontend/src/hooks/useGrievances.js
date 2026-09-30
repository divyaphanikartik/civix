import { useCallback, useEffect, useState } from "react";
import {
  getGrievances,
  getGrievance,
} from "../services/api";

export function useGrievances() {
  const [grievances, setGrievances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGrievances = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const data = await getGrievances();

      setGrievances(
        Array.isArray(data)
          ? data
          : data.items || []
      );
    } catch (err) {
      console.error(err);
      setError(err.message || "Unable to load grievances");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchGrievances();
  }, [fetchGrievances]);

  return {
    grievances,
    loading,
    error,
    refresh: fetchGrievances,
  };
}

export function useGrievance(id) {
  const [grievance, setGrievance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGrievance = useCallback(async () => {
    if (!id) return;

    try {
      setLoading(true);
      setError(null);

      const data = await getGrievance(id);

      setGrievance(data);
    } catch (err) {
      console.error(err);
      setError(err.message || "Unable to load grievance");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchGrievance();
  }, [fetchGrievance]);

  return {
    grievance,
    loading,
    error,
    refresh: fetchGrievance,
  };
}