import { INTENSITY_OPTIONS } from "./constants";
import L from "leaflet";

export function parseDurationToMinutes(duration) {
  if (!duration) return 0;
  let total = 0;
  const hours = duration.match(/(\d+)\s*h/);
  const mins  = duration.match(/(\d+)\s*min/);
  if (hours) total += parseInt(hours[1]) * 60;
  if (mins)  total += parseInt(mins[1]);
  return total;
}

export function formatMinutes(totalMinutes) {
  if (totalMinutes === 0) return "0 min";
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  if (h === 0) return `${m} min`;
  if (m === 0) return `${h}h`;
  return `${h}h ${m}min`;
}

export function formatDayDate(arrivalDate, dayIndex) {
  if (!arrivalDate) return null;
  const date = new Date(arrivalDate);
  date.setDate(date.getDate() + dayIndex);
  return date.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" });
}

export function buildDailyItinerary(attractions, numDays, intensityKey) {
  const config = INTENSITY_OPTIONS.find((o) => o.key === intensityKey);
  const maxMinPerDay = config.maxMinutesPerDay;
  const days = Array.from({ length: numDays }, () => ({ attractions: [], totalMinutes: 0 }));
  const overflow = [];

  for (const attraction of attractions) {
    const duration = parseDurationToMinutes(attraction.duration);
    const dayIndex = days.findIndex((day) =>
      day.totalMinutes + duration <= maxMinPerDay &&
      (config.maxAttractionsPerDay === null ||
        day.attractions.length < config.maxAttractionsPerDay)
    );
    if (dayIndex !== -1) {
      days[dayIndex].attractions.push(attraction);
      days[dayIndex].totalMinutes += duration;
    } else {
      overflow.push(attraction);
    }
  }
  return { days, overflow };
}

export function createMarkerIcon(color, label) {
  return L.divIcon({
    className: "",
    html: `<div style="background:${color};width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:13px;border:2px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);font-family:Arial,sans-serif">${label}</div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -18],
  });
}
