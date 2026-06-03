import { INTENSITY_OPTIONS, TRANSPORT_OPTIONS } from "./constants";
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

function timeToMinutes(timeStr) {
  const [h, m] = timeStr.split(":").map(Number);
  return h * 60 + m;
}

function minutesToTime(total) {
  const h = Math.floor(total / 60) % 24;
  const m = total % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
}

function recalculateItemTimes(items, startTimeStr) {
  let current = timeToMinutes(startTimeStr);
  return items.map((item) => {
    const duration = item.type === "attraction"
      ? parseDurationToMinutes(item.duration)
      : item.duration;
    const start_at = minutesToTime(current);
    current += duration;
    const end_at = minutesToTime(current);
    return { ...item, start_at, end_at };
  });
}

// Haversine distance in km
export function haversineKm(a1, a2) {
  if (!a1?.latitude || !a1?.longitude || !a2?.latitude || !a2?.longitude) return null;
  const R = 6371;
  const lat1 = a1.latitude * Math.PI / 180;
  const lat2 = a2.latitude * Math.PI / 180;
  const dLat = (a2.latitude - a1.latitude) * Math.PI / 180;
  const dLon = (a2.longitude - a1.longitude) * Math.PI / 180;
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// Haversine walking minutes, rounded UP to nearest 5
export function haversineMinutes(a1, a2, speedKmh = 5) {
  const km = haversineKm(a1, a2);
  if (km === null) return 0;
  const raw = (km / speedKmh) * 60;
  return Math.ceil(raw / 5) * 5;
}

export function computeTravelMinutes(attractions, speedKmh = 5) {
  return attractions.slice(0, -1).map((a, i) => haversineMinutes(a, attractions[i + 1], speedKmh));
}

export function computeTravelKm(attractions) {
  return attractions.slice(0, -1).map((a, i) => {
    const km = haversineKm(a, attractions[i + 1]);
    return km !== null ? Math.round(km * 100) / 100 : null;
  });
}

// Builds the flat items list for one day, inserting travel and break rows.
export function computeDayItems(attractions, travelMinutes, breakDurations, startTime, travelKm = []) {
  const rawItems = [];
  attractions.forEach((attr, i) => {
    rawItems.push({ type: "attraction", ...attr });
    if (i < attractions.length - 1) {
      const travel = travelMinutes[i] ?? 0;
      rawItems.push({
        type: "travel",
        id: `travel-${attr.id}`,
        duration: travel,
        gapIndex: i,
        distanceKm: travelKm[i] ?? null,
      });
      const breakDur = breakDurations[i];
      if (breakDur != null) {
        rawItems.push({ type: "break", id: `break-${attr.id}`, duration: breakDur, gapIndex: i });
      }
    }
  });
  return recalculateItemTimes(rawItems, startTime);
}

export function getTransportSpeed(transportMode) {
  return TRANSPORT_OPTIONS.find((o) => o.key === transportMode)?.speedKmh ?? 5;
}

export function buildDailyItinerary(
  attractions,
  numDays,
  intensityKey,
  startTime = "09:00",
  breakDurationMinutes = 30,
  transportMode = "walking"
) {
  const config = INTENSITY_OPTIONS.find((o) => o.key === intensityKey);
  const maxMinPerDay = config.maxMinutesPerDay;
  const isRelaxed = intensityKey === "relaxed";
  const speedKmh = getTransportSpeed(transportMode);

  const days = Array.from({ length: numDays }, () => ({
    attractions: [],
    travelMinutes: [],
    travelKm: [],
    breakDurations: [],
    items: [],
    totalMinutes: 0,
  }));
  const overflow = [];

  for (const attraction of attractions) {
    const duration = parseDurationToMinutes(attraction.duration);

    const dayIndex = days.findIndex((day) => {
      const last = day.attractions[day.attractions.length - 1];
      const travel = last ? haversineMinutes(last, attraction, speedKmh) : 0;
      const breakOverhead = isRelaxed && day.attractions.length > 0 ? breakDurationMinutes : 0;
      return (
        day.totalMinutes + travel + breakOverhead + duration <= maxMinPerDay &&
        (config.maxAttractionsPerDay === null || day.attractions.length < config.maxAttractionsPerDay)
      );
    });

    if (dayIndex !== -1) {
      const day = days[dayIndex];
      if (day.attractions.length > 0) {
        const last = day.attractions[day.attractions.length - 1];
        const travel = haversineMinutes(last, attraction, speedKmh);
        const km = haversineKm(last, attraction);
        day.travelMinutes.push(travel);
        day.travelKm.push(km !== null ? Math.round(km * 100) / 100 : null);
        day.totalMinutes += travel;
        day.breakDurations.push(isRelaxed ? breakDurationMinutes : null);
        if (isRelaxed) day.totalMinutes += breakDurationMinutes;
      }
      day.attractions.push(attraction);
      day.totalMinutes += duration;
    } else {
      overflow.push(attraction);
    }
  }

  const daysWithItems = days.map((day) => ({
    ...day,
    items: computeDayItems(day.attractions, day.travelMinutes, day.breakDurations, startTime, day.travelKm),
  }));

  return { days: daysWithItems, overflow };
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
