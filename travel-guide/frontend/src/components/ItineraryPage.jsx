import { INTENSITY_OPTIONS } from "../constants";
import { formatMinutes, formatDayDate } from "../utils";
import ItineraryMap from "./ItineraryMap";

export default function ItineraryPage({
  days, overflow, intensity, totalDuration,
  arrivalDate, numDays, departureDate,
  onBack, onChangeIntensity, onRegenerate,
  onMoveAttraction, onRemoveAttraction,
}) {
  return (
    <section className="itinerary">
      <button className="back" onClick={onBack}>← Back to Attractions</button>

      <div className="itinerary-header">
        <div>
          <h1>Your Travel Itinerary</h1>
          {arrivalDate && (
            <p>{arrivalDate} → {departureDate} · {numDays} {numDays === 1 ? "day" : "days"}</p>
          )}
        </div>
        <div className="total-duration">
          <span className="total-duration-label">Total duration</span>
          <span className="total-duration-value">{totalDuration}</span>
        </div>
      </div>

      <div className="intensity-switcher">
        <span className="intensity-switcher-label">Intensity:</span>
        {INTENSITY_OPTIONS.map((option) => (
          <button
            key={option.key}
            className={`intensity-chip${intensity === option.key ? " active" : ""}`}
            onClick={() => onChangeIntensity(option.key)}
          >
            {option.label}
          </button>
        ))}
        <button className="secondary regenerate-btn" onClick={onRegenerate}>
          Regenerate
        </button>
      </div>

      <div className="itinerary-map-panel">
        <ItineraryMap days={days} />
      </div>

      {days.map((day, dayIndex) => (
        <div key={dayIndex} className="day-block">
          <div className="day-header">
            <h2>
              Day {dayIndex + 1}
              {arrivalDate && (
                <span className="day-date"> — {formatDayDate(arrivalDate, dayIndex)}</span>
              )}
            </h2>
            <span className="day-duration">{formatMinutes(day.totalMinutes)}</span>
          </div>

          {day.attractions.length === 0 ? (
            <p className="day-empty">No attractions planned for this day.</p>
          ) : (
            <div className="itinerary-list">
              {day.attractions.flatMap((attraction, i) => {
                const isLast = i === day.attractions.length - 1;
                const item = (
                  <div key={attraction.id} className="itinerary-item">
                    <div className="itinerary-item-info">
                      <span className="itinerary-item-number">{i + 1}</span>
                      <div>
                        <strong>{attraction.name_en || attraction.name_pl}</strong>
                        <span className="itinerary-item-category">{attraction.category}</span>
                      </div>
                    </div>
                    <div className="itinerary-item-actions">
                      <span className="itinerary-item-duration">{attraction.duration}</span>
                      <div className="reorder-btns">
                        <button
                          className="reorder-btn"
                          onClick={() => onMoveAttraction(dayIndex, i, "up")}
                          disabled={i === 0}
                          title="Move up"
                        >↑</button>
                        <button
                          className="reorder-btn"
                          onClick={() => onMoveAttraction(dayIndex, i, "down")}
                          disabled={i === day.attractions.length - 1}
                          title="Move down"
                        >↓</button>
                      </div>
                      <button
                        className="remove-btn"
                        onClick={() => onRemoveAttraction(attraction.id)}
                        title="Remove"
                      >×</button>
                    </div>
                  </div>
                );
                const breakSlot = intensity === "relaxed" && !isLast ? (
                  <div key={`break-${attraction.id}`} className="downtime-slot">
                    <span>☕ Break</span>
                    <span>30 min</span>
                  </div>
                ) : null;
                return [item, breakSlot].filter(Boolean);
              })}
            </div>
          )}
        </div>
      ))}

      {overflow.length > 0 && (
        <div className="overflow-block">
          <div className="overflow-header">
            <h3>Didn't fit in your schedule ({overflow.length})</h3>
            <p>
              These attractions exceed your {numDays}-day <strong>{intensity}</strong> itinerary.
              Try switching to a more intense pace or adding more days.
            </p>
          </div>
          <div className="itinerary-list">
            {overflow.map((attraction) => (
              <div key={attraction.id} className="itinerary-item overflow-item">
                <div className="itinerary-item-info">
                  <div>
                    <strong>{attraction.name_en || attraction.name_pl}</strong>
                    <span className="itinerary-item-category">{attraction.category}</span>
                  </div>
                </div>
                <div className="itinerary-item-actions">
                  <span className="itinerary-item-duration">{attraction.duration}</span>
                  <button
                    className="remove-btn"
                    onClick={() => onRemoveAttraction(attraction.id)}
                    title="Remove"
                  >×</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
