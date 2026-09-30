import React, { useMemo, useState } from "react";
import PageContainer from "../components/layout/PageContainer";
import HotspotCard from "../components/hotspots/HotspotCard";
import { useHotspots } from "../hooks/useHotspots";

export default function Hotspots() {
  const {
    hotspots,
    loading,
    error,
  } = useHotspots();

  const [sector, setSector] = useState("ALL");
  const [minimumScore, setMinimumScore] = useState(0);

  const filteredHotspots = useMemo(() => {
    return hotspots.filter((hotspot) => {
      const sectorMatches =
        sector === "ALL" ||
        hotspot.sector === sector;

      const scoreMatches =
        Number(hotspot.total_score || 0) >=
        Number(minimumScore);

      return sectorMatches && scoreMatches;
    });
  }, [hotspots, sector, minimumScore]);

  const sectors = [
    ...new Set(
      hotspots
        .map((item) => item.sector)
        .filter(Boolean)
    ),
  ];

  return (
    <PageContainer
      title="Hotspots"
      subtitle="Infrastructure priority locations identified by Civix"
    >
      <div className="filter-bar">
        <div className="filter-group">
          <label>Sector</label>

          <select
            value={sector}
            onChange={(e) => setSector(e.target.value)}
          >
            <option value="ALL">All sectors</option>

            {sectors.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Minimum Score</label>

          <input
            type="number"
            min="0"
            max="100"
            value={minimumScore}
            onChange={(e) =>
              setMinimumScore(e.target.value)
            }
          />
        </div>

        <div className="filter-result-count">
          {filteredHotspots.length} hotspots
        </div>
      </div>

      {loading && (
        <div className="loading-state">
          Loading hotspots...
        </div>
      )}

      {error && (
        <div className="error-state">
          {error}
        </div>
      )}

      {!loading && !error && (
        <div className="hotspot-grid">
          {filteredHotspots.map((hotspot) => (
            <HotspotCard
              key={hotspot.id}
              hotspot={hotspot}
            />
          ))}
        </div>
      )}

      {!loading &&
        !error &&
        filteredHotspots.length === 0 && (
          <div className="empty-state">
            No hotspots match the selected filters.
          </div>
        )}
    </PageContainer>
  );
}