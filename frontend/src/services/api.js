const API_BASE_URL =
  import.meta.env.VITE_API_URL || "/api";

async function request(
  endpoint,
  options = {}
) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    }
  );

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      message || `Request failed: ${response.status}`
    );
  }

  return response.json();
}

export async function getHotspots() {
  return request("/hotspots");
}

export async function getHotspot(id) {
  return request(`/hotspots/${id}`);
}

export async function getGrievances() {
  return request("/grievances");
}

export async function getGrievance(id) {
  return request(`/grievances/${id}`);
}

export async function generateConceptNote(
  hotspotId
) {
  return request(
    `/projects/concept-note/${hotspotId}`,
    {
      method: "POST",
    }
  );
}