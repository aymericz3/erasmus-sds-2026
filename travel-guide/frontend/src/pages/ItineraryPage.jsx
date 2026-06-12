import { INTENSITY_OPTIONS, TRANSPORT_OPTIONS } from "../constants";
import { getItineraryScheduleValidation } from "../itineraryValidation";
import { formatMinutes, formatDayDate } from "../utils";
import ItineraryMap from "../components/ItineraryMap";

const TRANSPORT_ICONS = { walking: "🚶", cycling: "🚴", transit: "🚌" };

export default function ItineraryPage({
  days, overflow, intensity, totalDuration, transportMode,
  arrivalDate, numDays, departureDate,
  scheduleNotice,
  onBack, onChangeIntensity, onRegenerate,
  onMoveAttraction, onRemoveAttraction,
  onAddBreak, onRemoveBreak, onChangeBreakDuration,
  onShowAttractionDetails,
}) {
  const intensityConfig = INTENSITY_OPTIONS.find((o) => o.key === intensity);
  const scheduleValidation = getItineraryScheduleValidation(days, intensity);

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

      {scheduleNotice && (
        <div className="schedule-alert critical">
          {scheduleNotice}
        </div>
      )}

      {(scheduleValidation.blockers.length > 0 || scheduleValidation.warnings.length > 0) && (
        <div className={scheduleValidation.isValid ? "schedule-alert" : "schedule-alert critical"}>
          <strong>{scheduleValidation.isValid ? "Schedule warnings" : "Schedule needs attention"}</strong>
          <ul>
            {[...new Set([...scheduleValidation.blockers, ...scheduleValidation.warnings])].map((message) => (
              <li key={message}>{message}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="itinerary-map-panel">
        <ItineraryMap days={days} />
      </div>

      {days.map((day, dayIndex) => {
        let attrCounter = 0;
        const dayValidation = scheduleValidation.dayValidations[dayIndex];

        return (
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

            {day.totalMinutes > intensityConfig.maxMinutesPerDay && (
              <div className="day-warning">
                ⚠ This day is {formatMinutes(day.totalMinutes - intensityConfig.maxMinutesPerDay)} over
                your <strong>{intensityConfig.label}</strong> limit — shorten a break or remove an attraction.
              </div>
            )}

            {dayValidation?.blockers.length > 0 && (
              <div className="day-warning critical">
                <strong>Invalid schedule:</strong>
                <ul>
                  {dayValidation.blockers.map((message) => (
                    <li key={message}>{message}</li>
                  ))}
                </ul>
              </div>
            )}

            {dayValidation?.warnings.length > 0 && (
              <div className="day-warning">
                <strong>Schedule warning:</strong>
                <ul>
                  {dayValidation.warnings.map((message) => (
                    <li key={message}>{message}</li>
                  ))}
                </ul>
              </div>
            )}

            {day.items.length === 0 ? (
              <p className="day-empty">No attractions planned for this day.</p>
            ) : (
              <div className="itinerary-list">
                {day.items.map((item) => {
                  if (item.type === "travel") {
                    const hasBreak = day.breakDurations[item.gapIndex] != null;
                    const transportOption = TRANSPORT_OPTIONS.find((o) => o.key === transportMode);
                    const icon = TRANSPORT_ICONS[transportMode] ?? "🚶";
                    const modeLabel = transportOption?.label.toLowerCase() ?? "walk";
                    return (
                      <div key={item.id} className="travel-slot">
                        <div className="travel-slot-info">
                          {item.duration > 0 && (
                            <>
                              <span className="travel-icon">{icon}</span>
                              <span className="travel-label">{item.duration} min {modeLabel}</span>
                              {item.distanceKm !== null && item.distanceKm !== undefined && (
                                <span className="travel-distance">{item.distanceKm} km</span>
                              )}
                              {item.start_at && (
                                <span className="travel-time">{item.start_at} → {item.end_at}</span>
                              )}
                            </>
                          )}
                        </div>
                        {!hasBreak && (
                          <button
                            className="add-break-btn"
                            onClick={() => onAddBreak(dayIndex, item.gapIndex)}
                          >
                            + Break
                          </button>
                        )}
                      </div>
                    );
                  }

                  if (item.type === "break") {
                    return (
                      <div key={item.id} className="break-slot">
                        <div className="break-slot-label">
                          {item.start_at && (
                            <span className="break-time">{item.start_at} → {item.end_at}</span>
                          )}
                          <span className="break-icon">☕ Break</span>
                        </div>
                        <div className="break-slot-controls">
                          <button
                            className="break-adj-btn"
                            onClick={() => onChangeBreakDuration(dayIndex, item.gapIndex, -15)}
                            disabled={item.duration <= 15}
                          >−</button>
                          <span className="break-duration">{item.duration} min</span>
                          <button
                            className="break-adj-btn"
                            onClick={() => onChangeBreakDuration(dayIndex, item.gapIndex, +15)}
                            disabled={item.duration >= 120}
                          >+</button>
                          <button
                            className="remove-btn"
                            onClick={() => onRemoveBreak(dayIndex, item.gapIndex)}
                            title="Remove break"
                          >×</button>
                        </div>
                      </div>
                    );
                  }

                  const currentAttrIndex = attrCounter++;
                  const isFirstAttr = currentAttrIndex === 0;
                  const isLastAttr = currentAttrIndex === day.attractions.length - 1;

                  return (
                    <div key={item.id} className="itinerary-item">
                      {item.start_at && (
                        <span className="item-time-range">{item.start_at} → {item.end_at}</span>
                      )}
                      <div className="itinerary-item-info">
                        <span className="itinerary-item-number">{currentAttrIndex + 1}</span>
                        <div>
                          <strong>{item.name_en || item.name_pl}</strong>
                          <span className="itinerary-item-category">{item.category}</span>
                        </div>
                      </div>
                      <div className="itinerary-item-actions">
                        <span className="itinerary-item-duration">{item.duration}</span>
                        {onShowAttractionDetails && (
                          <button
                            className="info-btn"
                            onClick={() => onShowAttractionDetails(item)}
                            title="View details"
                          >ℹ</button>
                        )}
                        <div className="reorder-btns">
                          <button
                            className="reorder-btn"
                            onClick={() => onMoveAttraction(dayIndex, currentAttrIndex, "up")}
                            disabled={isFirstAttr}
                            title="Move up"
                          >↑</button>
                          <button
                            className="reorder-btn"
                            onClick={() => onMoveAttraction(dayIndex, currentAttrIndex, "down")}
                            disabled={isLastAttr}
                            title="Move down"
                          >↓</button>
                        </div>
                        <button
                          className="remove-btn"
                          onClick={() => onRemoveAttraction(item.id)}
                          title="Remove"
                        >×</button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}

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
                  {onShowAttractionDetails && (
                    <button
                      className="info-btn"
                      onClick={() => onShowAttractionDetails(attraction)}
                      title="View details"
                    >ℹ</button>
                  )}
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
