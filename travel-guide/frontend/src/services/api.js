const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });
  } catch {
    throw new Error("Network request failed");
  }

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json();
}

export function fetchPlaces() {
  return request("/places");
}

export function fetchCategories() {
  return request("/categories");
}

export async function savePreferences(preferences) {
  // TODO: Connect this to the backend preference save endpoint once PR #109 is confirmed ready.
  return {
    available: false,
    preferences,
    message: "Preference saving will be available once the backend endpoint is ready.",
  };
}

export async function loadPreferences() {
  // TODO: Connect this to the backend preference load endpoint once PR #109 is confirmed ready.
  return {
    available: false,
    preferences: null,
    message: "Preference loading will be available once the backend endpoint is ready.",
  };
}
