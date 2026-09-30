import React, { useState } from "react";
import PageContainer from "../src/components/layout/PageContainer";
import ProjectConceptNote from "../src/components/projects/ProjectConceptNote";
import { useHotspots } from "../hooks/useHotspots";
import { generateConceptNote } from "../src/services/api";

export default function Projects() {
  const { hotspots, loading } = useHotspots();

  const [selectedHotspot, setSelectedHotspot] =
    useState("");

  const [project, setProject] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  async function handleGenerate() {
    if (!selectedHotspot) return;

    try {
      setGenerating(true);
      setError(null);

      const result = await generateConceptNote(
        selectedHotspot
      );

      setProject(result);
    } catch (err) {
      console.error(err);
      setError(
        err.message ||
          "Unable to generate concept note"
      );
    } finally {
      setGenerating(false);
    }
  }

  return (
    <PageContainer
      title="Project Concept Notes"
      subtitle="Convert infrastructure hotspots into preliminary project proposals"
    >
      <div className="project-generator">
        <div className="filter-group">
          <label>Select hotspot</label>

          <select
            value={selectedHotspot}
            onChange={(e) =>
              setSelectedHotspot(e.target.value)
            }
            disabled={loading}
          >
            <option value="">
              Select a hotspot
            </option>

            {hotspots.map((hotspot) => (
              <option
                key={hotspot.id}
                value={hotspot.id}
              >
                {hotspot.hotspot_code} —{" "}
                {hotspot.panchayat ||
                  hotspot.district}
              </option>
            ))}
          </select>
        </div>

        <button
          className="primary-button"
          disabled={
            !selectedHotspot || generating
          }
          onClick={handleGenerate}
        >
          {generating
            ? "Generating..."
            : "Generate Concept Note"}
        </button>
      </div>

      {error && (
        <div className="error-state">
          {error}
        </div>
      )}

      {project && (
        <ProjectConceptNote project={project} />
      )}
    </PageContainer>
  );
}