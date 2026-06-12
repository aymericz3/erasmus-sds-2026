const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const DEFAULT_USER_ID = 1;

const FRONTEND_TO_BACKEND_INTENSITY = {
  relaxed: "low",
  moderate: "moderate",
  intense: "high",
};

const BACKEND_TO_FRONTEND_INTENSITY = {
  low: "relaxed",
  moderate: "moderate",
  high: "intense",
};

function getPreferenceUserId() {
  try {
    localStorage.setItem("travelPlannerUserId", String(DEFAULT_USER_ID));
  } catch {
    // localStorage can be unavailable in some browser privacy modes.
  }

  return DEFAULT_USER_ID;
}

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
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

export function planItinerary({
  place_ids,
  num_days = 1,
  intensity = "moderate",
  start_time = "09:00",
  end_time = "21:00",
  transport_mode = "walking",
  break_duration_minutes = 30,
}) {
  return request("/itinerary/plan", {
    method: "POST",
    body: JSON.stringify({
      place_ids,
      num_days,
      intensity,
      start_time,
      end_time,
      transport_mode,
      break_duration_minutes,
    }),
  });
}

export function fetchCategories() {
  return request("/categories");
}

export function savePreferences(preferences) {
  const payload = {
    user_id: getPreferenceUserId(),
    intensity: FRONTEND_TO_BACKEND_INTENSITY[preferences.intensity] ?? "moderate",
    transport_mode: preferences.transportMode ?? "walking",
    break_duration_minutes: preferences.breakDurationMinutes ?? 30,
    start_time: preferences.startTime ?? "09:00",
    selected_categories: preferences.selectedCategories ?? [],
  };

  return request("/preferences/save", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loadPreferences(userId = getPreferenceUserId()) {
  const data = await request(`/preferences/load/${userId}`);
  const preferences = data.preferences;

  return {
    ...data,
    preferences: preferences
      ? {
          selectedCategories: preferences.selected_categories ?? [],
          intensity: BACKEND_TO_FRONTEND_INTENSITY[preferences.intensity] ?? "moderate",
          transportMode: preferences.transport_mode ?? "walking",
          breakDurationMinutes: preferences.break_duration_minutes ?? 30,
          startTime: preferences.start_time ?? "09:00",
        }
      : null,
  };
}
