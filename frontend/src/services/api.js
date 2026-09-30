const API_BASE_URL =
  import.meta.env.VITE_API_URL || "/api";

async function request(endpoint, options = {}) {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    {
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
        ...(options.headers || {}),
      },
      ...options,
    }
  );

  const contentType =
    response.headers.get("content-type") || "";

  const responseText = await response.text();

  if (!response.ok) {
    throw new Error(
      responseText ||
        `Request failed: ${response.status}`
    );
  }

  if (!contentType.includes("application/json")) {
    throw new Error(
      `Expected JSON from ${API_BASE_URL}${endpoint}, but received ${contentType || "unknown content type"}`
    );
  }

  try {
    return JSON.parse(responseText);
  } catch {
    throw new Error(
      `Invalid JSON response from ${API_BASE_URL}${endpoint}`
    );
  }
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