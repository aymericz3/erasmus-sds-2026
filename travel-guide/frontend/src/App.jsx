import { useState, useEffect } from "react";
import "leaflet/dist/leaflet.css";

import { CATEGORIES } from "./constants";
import { parseDurationToMinutes, formatMinutes, buildDailyItinerary } from "./utils";
import HomePage from "./components/HomePage";
import ResultsPage from "./components/ResultsPage";
import ItineraryPage from "./components/ItineraryPage";

function App() {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [page, setPage] = useState("home");
  const [selectedAttractions, setSelectedAttractions] = useState([]);
  const [attractionsData, setAttractionsData] = useState([]);
  const [arrivalDate, setArrivalDate] = useState("");
  const [numDays, setNumDays] = useState(1);
  const [intensity, setIntensity] = useState("moderate");
  const [itineraryDays, setItineraryDays] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/places")
      .then((res) => res.json())
      .then(setAttractionsData)
      .catch((err) => console.error("Error loading places:", err));
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

  const generateItinerary = () => {
    setItineraryDays(buildDailyItinerary(selectedAttractions, numDays, intensity));
    setPage("itinerary");
  };

  const changeIntensity = (newIntensity) => {
    setIntensity(newIntensity);
    setItineraryDays(buildDailyItinerary(selectedAttractions, numDays, newIntensity));
  };

  const moveAttractionInDay = (dayIndex, attractionIndex, dir) => {
    const targetIndex = dir === "up" ? attractionIndex - 1 : attractionIndex + 1;
    setItineraryDays((prev) => {
      const day = prev.days[dayIndex];
      if (targetIndex < 0 || targetIndex >= day.attractions.length) return prev;
      const newAttractions = [...day.attractions];
      [newAttractions[attractionIndex], newAttractions[targetIndex]] =
        [newAttractions[targetIndex], newAttractions[attractionIndex]];
      return {
        ...prev,
        days: prev.days.map((d, i) => (i === dayIndex ? { ...d, attractions: newAttractions } : d)),
      };
    });
  };

  const removeFromItinerary = (attractionId) => {
    setSelectedAttractions((prev) => prev.filter((a) => a.id !== attractionId));
    setItineraryDays((prev) => {
      if (!prev) return prev;
      const newDays = prev.days.map((day) => {
        const newAttractions = day.attractions.filter((a) => a.id !== attractionId);
        return {
          ...day,
          attractions: newAttractions,
          totalMinutes: newAttractions.reduce((s, a) => s + parseDurationToMinutes(a.duration), 0),
        };
      });
      return { days: newDays, overflow: prev.overflow.filter((a) => a.id !== attractionId) };
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
          selectedCategories={selectedCategories}
          allCategoriesSelected={allCategoriesSelected}
          onArrivalDateChange={setArrivalDate}
          onNumDaysChange={setNumDays}
          onIntensityChange={setIntensity}
          onToggleCategory={toggleCategory}
          onToggleAllCategories={toggleAllCategories}
          onExplore={() => setPage("results")}
        />
      )}

      {page === "results" && (
        <ResultsPage
          attractions={filteredAttractions}
          selectedAttractions={selectedAttractions}
          selectedCategories={selectedCategories}
          allCategoriesSelected={allCategoriesSelected}
          onToggleAttraction={toggleAttraction}
          onToggleCategory={toggleCategory}
          onToggleAllCategories={toggleAllCategories}
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
          onChangeIntensity={changeIntensity}
          onRegenerate={generateItinerary}
          onMoveAttraction={moveAttractionInDay}
          onRemoveAttraction={removeFromItinerary}
        />
      )}
    </div>
  );
}

export default App;
