export const POZNAN_CENTER = [52.4064, 16.9252];

export const DAY_COLORS = ["#e63946", "#2a9d8f", "#f4a261", "#7b2d8b", "#1d78c1", "#e9c46a"];

export const CATEGORIES = [
  "culture", "art", "sport", "landmark",
  "family", "food", "outdoor", "hotel",
];

export const TRANSPORT_OPTIONS = [
  { key: "walking", label: "Walking", speedKmh: 5,  description: "~5 km/h on foot" },
  { key: "cycling", label: "Cycling", speedKmh: 15, description: "~15 km/h by bike" },
  { key: "transit", label: "Transit", speedKmh: 20, description: "~20 km/h by bus/tram" },
];

export const INTENSITY_OPTIONS = [
  { key: "relaxed",  label: "Relaxed",  description: "~4h/day · Max 3 attractions + breaks", maxMinutesPerDay: 240, maxAttractionsPerDay: 3 },
  { key: "moderate", label: "Moderate", description: "~6h/day · Balanced pace",               maxMinutesPerDay: 360, maxAttractionsPerDay: 5 },
  { key: "intense",  label: "Intense",  description: "~8h/day · Packed schedule",             maxMinutesPerDay: 480, maxAttractionsPerDay: null },
];
