import PreferencesPanel from "../components/PreferencesPanel";

export default function HomePage({
  arrivalDate, numDays, departureDate,
  intensity, startTime, endTime, transportMode, selectedCategories, allCategoriesSelected,
  preferenceStatus,
  onArrivalDateChange, onNumDaysChange, onIntensityChange, onStartTimeChange, onEndTimeChange,
  onTransportModeChange, onToggleCategory, onToggleAllCategories,
  onSavePreferences, onLoadPreferences, onExplore,
}) {
  return (
    <section className="home">
      <div className="badge">AI-Powered Travel Planning</div>
      <h1>Plan Your Perfect Trip</h1>
      <p className="subtitle">
        Discover amazing attractions in Poznan tailored to your interests.
        Select your preferences and let us create the perfect itinerary for you.
      </p>

      <PreferencesPanel
        arrivalDate={arrivalDate}
        numDays={numDays}
        departureDate={departureDate}
        intensity={intensity}
        startTime={startTime}
        endTime={endTime}
        transportMode={transportMode}
        selectedCategories={selectedCategories}
        allCategoriesSelected={allCategoriesSelected}
        preferenceStatus={preferenceStatus}
        onArrivalDateChange={onArrivalDateChange}
        onNumDaysChange={onNumDaysChange}
        onIntensityChange={onIntensityChange}
        onStartTimeChange={onStartTimeChange}
        onEndTimeChange={onEndTimeChange}
        onTransportModeChange={onTransportModeChange}
        onToggleCategory={onToggleCategory}
        onToggleAllCategories={onToggleAllCategories}
        onSavePreferences={onSavePreferences}
        onLoadPreferences={onLoadPreferences}
      />

      <div className="actions">
        <button className="primary" onClick={onExplore}>Explore Attractions</button>
      </div>
    </section>
  );
}
