import { useState, useEffect, useCallback } from "react";
import "leaflet/dist/leaflet.css";

import { CATEGORIES } from "./constants";
import {
  parseDurationToMinutes, formatMinutes,
  buildDailyItinerary, computeDayItems, computeTravelMinutes, computeTravelKm,
  getTransportSpeed,
} from "./utils";
import { getDayScheduleValidation } from "./itineraryValidation";
import { fetchPlaces, loadPreferences, savePreferences } from "./services/api";
import AttractionDetailsModal from "./components/AttractionDetailsModal";
import HomePage from "./pages/HomePage";
import ResultsPage from "./pages/ResultsPage";
import ItineraryPage from "./pages/ItineraryPage";

function totalFromItems(items) {
  return items.reduce(
    (s, item) => s + (item.type === "attraction" ? parseDurationToMinutes(item.duration) : item.duration),
    0
  );
}

function App() {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [page, setPage] = useState("home");
  const [selectedAttractions, setSelectedAttractions] = useState([]);
  const [attractionsData, setAttractionsData] = useState([]);
  const [isLoadingAttractions, setIsLoadingAttractions] = useState(true);
  const [attractionsError, setAttractionsError] = useState(null);
  const [selectedAttractionDetails, setSelectedAttractionDetails] = useState(null);
  const [preferenceStatus, setPreferenceStatus] = useState("");
  const [arrivalDate, setArrivalDate] = useState("");
  const [numDays, setNumDays] = useState(1);
  const [intensity, setIntensity] = useState("moderate");
  const [startTime, setStartTime] = useState("09:00");
  const [transportMode, setTransportMode] = useState("walking");
  const [itineraryDays, setItineraryDays] = useState(null);
  const [scheduleNotice, setScheduleNotice] = useState("");

  const retryLoadAttractions = useCallback(async () => {
    setIsLoadingAttractions(true);
    setAttractionsError(null);

    try {
      const places = await fetchPlaces();
      setAttractionsData(Array.isArray(places) ? places : []);
    } catch {
      setAttractionsData([]);
      setAttractionsError("Could not load attractions. Please check that the backend is running.");
    } finally {
      setIsLoadingAttractions(false);
    }
  }, []);

  useEffect(() => {
    let isActive = true;

    async function loadInitialAttractions() {
      try {
        const places = await fetchPlaces();
        if (isActive) setAttractionsData(Array.isArray(places) ? places : []);
      } catch {
        if (isActive) {
          setAttractionsData([]);
          setAttractionsError("Could not load attractions. Please check that the backend is running.");
        }
      } finally {
        if (isActive) setIsLoadingAttractions(false);
      }
    }

    loadInitialAttractions();

    return () => {
      isActive = false;
    };
  }, []);

  const allCategoriesSelected = selectedCategories.length === CATEGORIES.length;

  const toggleCategory = (category) => {
    setSelectedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c !== category) : [...prev, category]
    );
  };

  const toggleAllCategories = () => {
    setSelectedCategories(allCategoriesSelected ? [] : CATEGORIES);
  };

  const filteredAttractions =
    selectedCategories.length === 0
      ? attractionsData
      : attractionsData.filter((a) => selectedCategories.includes(a.category));

  const toggleAttraction = (attraction) => {
    setSelectedAttractions((prev) => {
      const exists = prev.some((a) => a.id === attraction.id);
      return exists ? prev.filter((a) => a.id !== attraction.id) : [...prev, attraction];
    });
  };

  const totalMinutes = selectedAttractions.reduce(
    (sum, a) => sum + parseDurationToMinutes(a.duration), 0
  );

  const departureDate = arrivalDate
    ? new Date(new Date(arrivalDate).getTime() + numDays * 24 * 60 * 60 * 1000)
        .toISOString().split("T")[0]
    : null;

  const currentPreferences = {
    selectedCategories,
    startTime,
    intensity,
    transportMode,
    breakDurationMinutes: 30,
  };

  const handleSavePreferences = async () => {
    try {
      await savePreferences(currentPreferences);
      setPreferenceStatus("Preferences saved successfully.");
    } catch {
      setPreferenceStatus("Could not save preferences. Please check that the backend is running.");
    }
  };

  const handleLoadPreferences = async () => {
    try {
      const result = await loadPreferences(1);

      if (result.preferences) {
        setSelectedCategories(result.preferences.selectedCategories ?? []);
        setStartTime(result.preferences.startTime ?? "09:00");
        setIntensity(result.preferences.intensity ?? "moderate");
        setTransportMode(result.preferences.transportMode ?? "walking");
      }

      setPreferenceStatus(
        result.is_new_user
          ? "No saved preferences found yet. You can create them now."
          : "Preferences loaded successfully."
      );
    } catch {
      setPreferenceStatus("Could not load preferences. Please check that the backend is running.");
    }
  };

  const generateItinerary = () => {
    setItineraryDays(buildDailyItinerary(selectedAttractions, numDays, intensity, startTime, 30, transportMode));
    setScheduleNotice("");
    setPage("itinerary");
  };

  const changeIntensity = (newIntensity) => {
    setIntensity(newIntensity);
    setItineraryDays(buildDailyItinerary(selectedAttractions, numDays, newIntensity, startTime, 30, transportMode));
    setScheduleNotice("");
  };

  const buildUpdatedDay = (day, newAttractions, newBreakDurations) => {
    const speed = getTransportSpeed(transportMode);
    const newTravelMinutes = computeTravelMinutes(newAttractions, speed);
    const newTravelKm = computeTravelKm(newAttractions);
    const newItems = computeDayItems(newAttractions, newTravelMinutes, newBreakDurations, startTime, newTravelKm);
    return {
      ...day,
      attractions: newAttractions,
      travelMinutes: newTravelMinutes,
      travelKm: newTravelKm,
      breakDurations: newBreakDurations,
      items: newItems,
      totalMinutes: totalFromItems(newItems),
    };
  };

  const applyDayUpdate = (dayIndex, updatedDay, actionLabel) => {
    const validation = getDayScheduleValidation(updatedDay, intensity);
    if (!validation.isValid) {
      setScheduleNotice(`${actionLabel} was not applied: ${validation.blockers[0]}`);
      return;
    }

    setScheduleNotice("");
    setItineraryDays((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        days: prev.days.map((day, index) => (index === dayIndex ? updatedDay : day)),
      };
    });
  };

  const moveAttractionInDay = (dayIndex, attractionIndex, dir) => {
    const day = itineraryDays?.days[dayIndex];
    if (!day) return;

    const targetIndex = dir === "up" ? attractionIndex - 1 : attractionIndex + 1;
    if (targetIndex < 0 || targetIndex >= day.attractions.length) return;

    const newAttractions = [...day.attractions];
    [newAttractions[attractionIndex], newAttractions[targetIndex]] =
      [newAttractions[targetIndex], newAttractions[attractionIndex]];
    const updatedDay = buildUpdatedDay(day, newAttractions, [...day.breakDurations]);
    applyDayUpdate(dayIndex, updatedDay, "Reorder");
  };

  const removeFromItinerary = (attractionId) => {
    setScheduleNotice("");
    setSelectedAttractions((prev) => prev.filter((a) => a.id !== attractionId));
    setItineraryDays((prev) => {
      if (!prev) return prev;
      const newDays = prev.days.map((day) => {
        const attrIndex = day.attractions.findIndex((a) => a.id === attractionId);
        if (attrIndex === -1) return day;
        const newAttractions = day.attractions.filter((a) => a.id !== attractionId);
        const newBreakDurations = [...day.breakDurations];
        if (attrIndex === 0) {
          newBreakDurations.splice(0, 1);
        } else if (attrIndex === day.attractions.length - 1) {
          newBreakDurations.splice(attrIndex - 1, 1);
        } else {
          newBreakDurations.splice(attrIndex - 1, 2, null);
        }
        const speed = getTransportSpeed(transportMode);
        const newTravelMinutes = computeTravelMinutes(newAttractions, speed);
        const newTravelKm = computeTravelKm(newAttractions);
        const newItems = computeDayItems(newAttractions, newTravelMinutes, newBreakDurations, startTime, newTravelKm);
        return { ...day, attractions: newAttractions, travelMinutes: newTravelMinutes, travelKm: newTravelKm, breakDurations: newBreakDurations, items: newItems, totalMinutes: totalFromItems(newItems) };
      });
      return { days: newDays, overflow: prev.overflow.filter((a) => a.id !== attractionId) };
    });
  };

  const addBreak = (dayIndex, gapIndex) => {
    const day = itineraryDays?.days[dayIndex];
    if (!day) return;

    const newBreakDurations = [...day.breakDurations];
    newBreakDurations[gapIndex] = 30;
    const updatedDay = buildUpdatedDay(day, day.attractions, newBreakDurations);
    applyDayUpdate(dayIndex, updatedDay, "Break");
  };

  const removeBreak = (dayIndex, gapIndex) => {
    const day = itineraryDays?.days[dayIndex];
    if (!day) return;

    const newBreakDurations = [...day.breakDurations];
    newBreakDurations[gapIndex] = null;
    const updatedDay = buildUpdatedDay(day, day.attractions, newBreakDurations);
    setScheduleNotice("");
    setItineraryDays((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        days: prev.days.map((currentDay, index) => (index === dayIndex ? updatedDay : currentDay)),
      };
    });
  };

  const changeBreakDuration = (dayIndex, gapIndex, delta) => {
    const day = itineraryDays?.days[dayIndex];
    if (!day) return;

    const newBreakDurations = [...day.breakDurations];
    newBreakDurations[gapIndex] = Math.max(15, Math.min(120, (newBreakDurations[gapIndex] ?? 30) + delta));
    const updatedDay = buildUpdatedDay(day, day.attractions, newBreakDurations);

    if (delta > 0) {
      applyDayUpdate(dayIndex, updatedDay, "Break duration change");
      return;
    }

    setScheduleNotice("");
    setItineraryDays((prev) => {
      if (!prev) return prev;
      return {
        ...prev,
        days: prev.days.map((currentDay, index) => (index === dayIndex ? updatedDay : currentDay)),
      };
    });
  };

  return (
    <div className="app">
      {page === "home" && (
        <HomePage
          arrivalDate={arrivalDate}
          numDays={numDays}
          departureDate={departureDate}
          intensity={intensity}
          startTime={startTime}
          selectedCategories={selectedCategories}
          allCategoriesSelected={allCategoriesSelected}
          onArrivalDateChange={setArrivalDate}
          onNumDaysChange={setNumDays}
          onIntensityChange={setIntensity}
          onStartTimeChange={setStartTime}
          transportMode={transportMode}
          onTransportModeChange={setTransportMode}
          onToggleCategory={toggleCategory}
          onToggleAllCategories={toggleAllCategories}
          preferenceStatus={preferenceStatus}
          onSavePreferences={handleSavePreferences}
          onLoadPreferences={handleLoadPreferences}
          onExplore={() => setPage("results")}
        />
      )}

      {page === "results" && (
        <ResultsPage
          attractions={filteredAttractions}
          selectedAttractions={selectedAttractions}
          selectedCategories={selectedCategories}
          allCategoriesSelected={allCategoriesSelected}
          isLoadingAttractions={isLoadingAttractions}
          attractionsError={attractionsError}
          onRetryAttractions={retryLoadAttractions}
          onToggleAttraction={toggleAttraction}
          onToggleCategory={toggleCategory}
          onToggleAllCategories={toggleAllCategories}
          onShowAttractionDetails={setSelectedAttractionDetails}
          onBack={() => setPage("home")}
          onGenerateItinerary={generateItinerary}
        />
      )}

      {page === "itinerary" && (
        <ItineraryPage
          days={itineraryDays?.days ?? []}
          overflow={itineraryDays?.overflow ?? []}
          intensity={intensity}
          totalDuration={formatMinutes(totalMinutes)}
          arrivalDate={arrivalDate}
          numDays={numDays}
          departureDate={departureDate}
          onBack={() => setPage("results")}
          transportMode={transportMode}
          scheduleNotice={scheduleNotice}
          onChangeIntensity={changeIntensity}
          onRegenerate={generateItinerary}
          onMoveAttraction={moveAttractionInDay}
          onRemoveAttraction={removeFromItinerary}
          onAddBreak={addBreak}
          onRemoveBreak={removeBreak}
          onChangeBreakDuration={changeBreakDuration}
        />
      )}

      <AttractionDetailsModal
        attraction={selectedAttractionDetails}
        onClose={() => setSelectedAttractionDetails(null)}
      />
    </div>
  );
}

export default App;
