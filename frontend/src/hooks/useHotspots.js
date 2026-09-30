import { useCallback, useEffect, useState } from "react";

import { getHotspots } from "../services/api";

export function useHotspots() {
  const [hotspots, setHotspots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async (showLoading = false) => {
    if (showLoading) {
      setLoading(true);
    }

    try {
      const data = await getHotspots();
      setHotspots(data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      if (showLoading) {
        setLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    load(true);

    // Keep the dashboard current while WhatsApp grievances are processed
    // asynchronously by the backend worker.
    const interval = setInterval(() => load(false), 5000);

    return () => clearInterval(interval);
  }, [load]);

  return {
    hotspots,
    loading,
    error,
    refresh: () => load(true),
  };
}
