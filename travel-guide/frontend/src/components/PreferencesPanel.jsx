import { CATEGORIES, INTENSITY_OPTIONS, TRANSPORT_OPTIONS } from "../constants";

export default function PreferencesPanel({
  arrivalDate,
  numDays,
  departureDate,
  intensity,
  startTime,
  transportMode,
  selectedCategories,
  allCategoriesSelected,
  preferenceStatus,
  onArrivalDateChange,
  onNumDaysChange,
  onIntensityChange,
  onStartTimeChange,
  onTransportModeChange,
  onToggleCategory,
  onToggleAllCategories,
  onSavePreferences,
  onLoadPreferences,
}) {
  return (
    <>
      <div className="panel">
        <h2>Your Stay in Poznan</h2>
        <p>Tell us when and how long you are visiting</p>
        <div className="stay-inputs">
          <div className="stay-field">
            <label htmlFor="arrival">Arrival date</label>
            <input id="arrival" type="date" value={arrivalDate} onChange={(e) => onArrivalDateChange(e.target.value)} />
          </div>
          <div className="stay-field">
            <label htmlFor="days">Number of days</label>
            <input
              id="days" type="number" min="1" max="30" value={numDays}
              onChange={(e) => onNumDaysChange(Math.max(1, parseInt(e.target.value) || 1))}
            />
          </div>
          <div className="stay-field">
            <label htmlFor="start-time">Daily start time</label>
            <input
              id="start-time" type="time" value={startTime}
              onChange={(e) => onStartTimeChange(e.target.value)}
            />
          </div>
          {arrivalDate && (
            <div className="stay-summary">
              {arrivalDate} to {departureDate} - {numDays} {numDays === 1 ? "day" : "days"} - starts at {startTime}
            </div>
          )}
        </div>
      </div>

      <div className="panel">
        <h2>Trip Intensity</h2>
        <p>How packed do you want your days to be?</p>
        <div className="intensity-options">
          {INTENSITY_OPTIONS.map((option) => (
            <button
              key={option.key}
              className={`intensity-card${intensity === option.key ? " active" : ""}`}
              onClick={() => onIntensityChange(option.key)}
            >
              <span className="intensity-label">{option.label}</span>
              <span className="intensity-desc">{option.description}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="panel">
        <h2>How will you get around?</h2>
        <p>This affects travel time estimates between attractions</p>
        <div className="transport-options">
          {TRANSPORT_OPTIONS.map((option) => (
            <button
              key={option.key}
              className={`transport-card${transportMode === option.key ? " active" : ""}`}
              onClick={() => onTransportModeChange(option.key)}
            >
              <span className="transport-label">{option.label}</span>
              <span className="transport-desc">{option.description}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="panel">
        <h2>Select Your Interests</h2>
        <p>Choose categories that match your travel style</p>
        <div className="categories">
          <button
            className={allCategoriesSelected ? "category active" : "category"}
            onClick={onToggleAllCategories}
          >
            All
          </button>
          {CATEGORIES.map((category) => (
            <button
              key={category}
              className={selectedCategories.includes(category) ? "category active" : "category"}
              onClick={() => onToggleCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>

        <div className="preference-actions">
          <button className="secondary" onClick={onSavePreferences}>Save Preferences</button>
          <button className="secondary" onClick={onLoadPreferences}>Load Preferences</button>
        </div>
        {preferenceStatus && <p className="preference-status">{preferenceStatus}</p>}
      </div>
    </>
  );
}
