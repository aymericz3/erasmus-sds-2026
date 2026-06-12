import { INTENSITY_OPTIONS } from "./constants";

const LATEST_REASONABLE_END = 22 * 60;
const MIDNIGHT = 24 * 60;
const LONG_TRAVEL_MINUTES = 90;

function timeToMinutes(timeStr) {
  if (!timeStr || !/^\d{2}:\d{2}$/.test(timeStr)) return null;
  const [hours, minutes] = timeStr.split(":").map(Number);
  return hours * 60 + minutes;
}

function formatClock(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}`;
}

function getIntensityConfig(intensityKey) {
  return INTENSITY_OPTIONS.find((option) => option.key === intensityKey) ?? INTENSITY_OPTIONS[1];
}

export function getDayScheduleValidation(day, intensityKey) {
  const config = getIntensityConfig(intensityKey);
  const blockers = [];
  const warnings = [];

  if (!day) {
    return { blockers, warnings, isValid: true };
  }

  if (day.totalMinutes > config.maxMinutesPerDay) {
    blockers.push(
      `This day is over the ${config.label.toLowerCase()} limit. Shorten breaks, remove an attraction, or choose a higher intensity.`
    );
  }

  if (day.items.length === 0) {
    warnings.push("No attractions are planned for this day.");
  }

  let previousEnd = null;
  day.items.forEach((item) => {
    const start = timeToMinutes(item.start_at);
    const end = timeToMinutes(item.end_at);

    if (start !== null && end !== null) {
      const adjustedEnd = end < start ? end + MIDNIGHT : end;

      if (previousEnd !== null && start < previousEnd) {
        blockers.push("This schedule has overlapping time slots.");
      }

      if (adjustedEnd >= MIDNIGHT) {
        blockers.push("This schedule continues past midnight.");
      } else if (adjustedEnd > LATEST_REASONABLE_END) {
        warnings.push(`This schedule ends late (${formatClock(adjustedEnd)}).`);
      }

      previousEnd = adjustedEnd;
    }

    if (item.type === "travel" && item.duration >= LONG_TRAVEL_MINUTES) {
      warnings.push(`A travel segment takes ${item.duration} minutes, which may be unrealistic for a compact day.`);
    }
  });

  return {
    blockers: [...new Set(blockers)],
    warnings: [...new Set(warnings)],
    isValid: blockers.length === 0,
  };
}

export function getItineraryScheduleValidation(days, intensityKey) {
  const dayValidations = days.map((day) => getDayScheduleValidation(day, intensityKey));
  return {
    dayValidations,
    blockers: dayValidations.flatMap((validation) => validation.blockers),
    warnings: dayValidations.flatMap((validation) => validation.warnings),
    isValid: dayValidations.every((validation) => validation.isValid),
  };
}
