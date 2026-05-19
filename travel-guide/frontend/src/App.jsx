
import { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const POZNAN_CENTER = [52.4064, 16.9252];
const DAY_COLORS = ["#e63946", "#2a9d8f", "#f4a261", "#7b2d8b", "#1d78c1", "#e9c46a"];

const categories = [
  "culture", "art", "sport", "landmark",
  "family", "food", "outdoor", "hotel",
];

const INTENSITY_OPTIONS = [
  { key: "relaxed",  label: "Relaxed",  description: "~4h/day · Few attractions, plenty of breaks", maxMinutesPerDay: 240 },
  { key: "moderate", label: "Moderate", description: "~6h/day · Balanced pace",                     maxMinutesPerDay: 360 },
  { key: "intense",  label: "Intense",  description: "~8h/day · Packed schedule",                   maxMinutesPerDay: 480 },
];

function parseDurationToMinutes(duration) {
  if (!duration) return 0;
  let total = 0;
  const hours = duration.match(/(\d+)\s*h/);
  const mins  = duration.match(/(\d+)\s*min/);
  if (hours) total += parseInt(hours[1]) * 60;
  if (mins)  total += parseInt(mins[1]);
  return total;
}

function formatMinutes(totalMinutes) {
  if (totalMinutes === 0) return "0 min";
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  if (h === 0) return `${m} min`;
  if (m === 0) return `${h}h`;
  return `${h}h ${m}min`;
}

function formatDayDate(arrivalDate, dayIndex) {
  if (!arrivalDate) return null;
  const date = new Date(arrivalDate);
  date.setDate(date.getDate() + dayIndex);
  return date.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" });
}

function buildDailyItinerary(attractions, numDays, intensityKey) {
  const config = INTENSITY_OPTIONS.find((o) => o.key === intensityKey);
  const maxMinPerDay = config.maxMinutesPerDay;
  const days = Array.from({ length: numDays }, () => ({ attractions: [], totalMinutes: 0 }));
  const overflow = [];

  for (const attraction of attractions) {
    const duration = parseDurationToMinutes(attraction.duration);
    const dayIndex = days.findIndex((day) => day.totalMinutes + duration <= maxMinPerDay);
    if (dayIndex !== -1) {
      days[dayIndex].attractions.push(attraction);
      days[dayIndex].totalMinutes += duration;
    } else {
      overflow.push(attraction);
    }
  }
  return { days, overflow };
}

function createMarkerIcon(color, label) {
  return L.divIcon({
    className: "",
    html: `<div style="background:${color};width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:13px;border:2px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.3);font-family:Arial,sans-serif">${label}</div>`,
    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -18],
  });
}

function ResultsMap({ attractions, selectedAttractions, onToggle }) {
  const located = attractions.filter((a) => a.latitude && a.longitude);
  if (located.length === 0) {
    return <div className="map-empty">No location data available</div>;
  }
  return (
    <MapContainer center={POZNAN_CENTER} zoom={13} style={{ height: "100%", width: "100%" }} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {located.map((attraction) => {
        const isSelected = selectedAttractions.some((a) => a.id === attraction.id);
        return (
          <Marker
            key={attraction.id}
            position={[attraction.latitude, attraction.longitude]}
            icon={createMarkerIcon(isSelected ? "#060617" : "#9ca3af", isSelected ? "✓" : "·")}
            eventHandlers={{ click: () => onToggle(attraction) }}
          >
            <Popup>
              <strong>{attraction.name_en || attraction.name_pl}</strong>
              <br />{attraction.category} · {attraction.duration}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}

function ItineraryMap({ days }) {
  const hasCoords = days.some((d) => d.attractions.some((a) => a.latitude && a.longitude));
  if (!hasCoords) return null;
  return (
    <MapContainer center={POZNAN_CENTER} zoom={13} style={{ height: "100%", width: "100%" }} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {days.flatMap((day, dayIndex) => {
        const color = DAY_COLORS[dayIndex % DAY_COLORS.length];
        const located = day.attractions.filter((a) => a.latitude && a.longitude);
        const positions = located.map((a) => [a.latitude, a.longitude]);
        return [
          ...located.map((a, i) => (
            <Marker key={`m-${a.id}`} position={[a.latitude, a.longitude]} icon={createMarkerIcon(color, i + 1)}>
              <Popup>
                <strong>Day {dayIndex + 1} · Stop {i + 1}</strong>
                <br />{a.name_en || a.name_pl}
                <br />{a.duration}
              </Popup>
            </Marker>
          )),
          positions.length > 1 && (
            <Polyline key={`r-${dayIndex}`} positions={positions} color={color} weight={3} opacity={0.7} dashArray="8 4" />
          ),
        ].filter(Boolean);
      })}
    </MapContainer>
  );
}

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

  const allCategoriesSelected = selectedCategories.length === categories.length;

  const toggleCategory = (category) => {
    setSelectedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c !== category) : [...prev, category]
    );
  };

  const toggleAllCategories = () => {
    setSelectedCategories(allCategoriesSelected ? [] : categories);
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

  const currentDays = itineraryDays?.days ?? [];
  const currentOverflow = itineraryDays?.overflow ?? [];

  return (
    <div className="app">
      {/* ── HOME ── */}
      {page === "home" && (
        <section className="home">
          <div className="badge">AI-Powered Travel Planning</div>
          <h1>Plan Your Perfect Trip</h1>
          <p className="subtitle">
            Discover amazing attractions in Poznań tailored to your interests.
            Select your preferences and let us create the perfect itinerary for you.
          </p>

          <div className="panel">
            <h2>Your Stay in Poznań</h2>
            <p>Tell us when and how long you are visiting</p>
            <div className="stay-inputs">
              <div className="stay-field">
                <label htmlFor="arrival">Arrival date</label>
                <input id="arrival" type="date" value={arrivalDate} onChange={(e) => setArrivalDate(e.target.value)} />
              </div>
              <div className="stay-field">
                <label htmlFor="days">Number of days</label>
                <input
                  id="days" type="number" min="1" max="30" value={numDays}
                  onChange={(e) => setNumDays(Math.max(1, parseInt(e.target.value) || 1))}
                />
              </div>
              {arrivalDate && (
                <div className="stay-summary">
                  {arrivalDate} → {departureDate} · {numDays} {numDays === 1 ? "day" : "days"}
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
                  onClick={() => setIntensity(option.key)}
                >
                  <span className="intensity-label">{option.label}</span>
                  <span className="intensity-desc">{option.description}</span>
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
                onClick={toggleAllCategories}
              >
                All
              </button>
              {categories.map((category) => (
                <button
                  key={category}
                  className={selectedCategories.includes(category) ? "category active" : "category"}
                  onClick={() => toggleCategory(category)}
                >
                  {category}
                </button>
              ))}
            </div>
            <div className="actions">
              <button className="primary" onClick={() => setPage("results")}>
                Explore Attractions →
              </button>
            </div>
          </div>
        </section>
      )}

      {/* ── RESULTS ── */}
      {page === "results" && (
        <section className="results">
          <button className="back" onClick={() => setPage("home")}>← Back to Categories</button>

          <div className="results-header">
            <div>
              <h1>Available Attractions</h1>
              <p>{selectedAttractions.length} attractions selected</p>
            </div>
            <button
              className="primary"
              disabled={selectedAttractions.length === 0}
              onClick={generateItinerary}
            >
              Generate Itinerary
            </button>
          </div>

          <div className="filters">
            <button
              className={allCategoriesSelected ? "category active" : "category"}
              onClick={toggleAllCategories}
            >
              All
            </button>
            {categories.map((category) => (
              <button
                key={category}
                className={selectedCategories.includes(category) ? "category active" : "category"}
                onClick={() => toggleCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>

          <div className="results-layout">
            <div className="cards">
              {filteredAttractions.map((attraction) => {
                const isSelected = selectedAttractions.some((a) => a.id === attraction.id);
                return (
                  <div key={attraction.id} className={isSelected ? "card selected" : "card"}>
                    <img src={attraction.image_url} alt={attraction.name_en} />
                    <div className="card-body">
                      <div className="tags"><span>{attraction.category}</span></div>
                      <h3>{attraction.name_en || attraction.name_pl}</h3>
                      <p>{attraction.description}</p>
                      <div className="info">
                        <span>{attraction.duration}</span>
                        <span>{attraction.price_range}</span>
                      </div>
                      <button
                        className={isSelected ? "selected-btn" : "select-btn"}
                        onClick={() => toggleAttraction(attraction)}
                      >
                        {isSelected ? "Selected" : "Select"}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="results-map-panel">
              <ResultsMap
                attractions={filteredAttractions}
                selectedAttractions={selectedAttractions}
                onToggle={toggleAttraction}
              />
            </div>
          </div>
        </section>
      )}

      {/* ── ITINERARY ── */}
      {page === "itinerary" && (
        <section className="itinerary">
          <button className="back" onClick={() => setPage("results")}>← Back to Attractions</button>

          <div className="itinerary-header">
            <div>
              <h1>Your Travel Itinerary</h1>
              {arrivalDate && (
                <p>{arrivalDate} → {departureDate} · {numDays} {numDays === 1 ? "day" : "days"}</p>
              )}
            </div>
            <div className="total-duration">
              <span className="total-duration-label">Total duration</span>
              <span className="total-duration-value">{formatMinutes(totalMinutes)}</span>
            </div>
          </div>

          <div className="intensity-switcher">
            <span className="intensity-switcher-label">Intensity:</span>
            {INTENSITY_OPTIONS.map((option) => (
              <button
                key={option.key}
                className={`intensity-chip${intensity === option.key ? " active" : ""}`}
                onClick={() => changeIntensity(option.key)}
              >
                {option.label}
              </button>
            ))}
            <button className="secondary regenerate-btn" onClick={generateItinerary}>
              Regenerate
            </button>
          </div>

          <div className="itinerary-map-panel">
            <ItineraryMap days={currentDays} />
          </div>

          {currentDays.map((day, dayIndex) => (
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
                  {day.attractions.map((attraction, i) => (
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
                            onClick={() => moveAttractionInDay(dayIndex, i, "up")}
                            disabled={i === 0}
                            title="Move up"
                          >↑</button>
                          <button
                            className="reorder-btn"
                            onClick={() => moveAttractionInDay(dayIndex, i, "down")}
                            disabled={i === day.attractions.length - 1}
                            title="Move down"
                          >↓</button>
                        </div>
                        <button
                          className="remove-btn"
                          onClick={() => removeFromItinerary(attraction.id)}
                          title="Remove"
                        >×</button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}

          {currentOverflow.length > 0 && (
            <div className="overflow-block">
              <div className="overflow-header">
                <h3>Didn't fit in your schedule ({currentOverflow.length})</h3>
                <p>
                  These attractions exceed your {numDays}-day <strong>{intensity}</strong> itinerary.
                  Try switching to a more intense pace or adding more days.
                </p>
              </div>
              <div className="itinerary-list">
                {currentOverflow.map((attraction) => (
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
                        onClick={() => removeFromItinerary(attraction.id)}
                        title="Remove"
                      >×</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default App;
