
import { useState, useEffect } from "react";
 
const categories = [
  "culture",
  "art",
  "sport",
  "landmark",
  "family",
  "food",
  "outdoor",
  "hotel",
];
 
function parseDurationToMinutes(duration) {
  if (!duration) return 0;
  let total = 0;
  const hours = duration.match(/(\d+)\s*h/);
  const mins = duration.match(/(\d+)\s*min/);
  if (hours) total += parseInt(hours[1]) * 60;
  if (mins) total += parseInt(mins[1]);
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
 
function App() {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [page, setPage] = useState("home");
  const [selectedAttractions, setSelectedAttractions] = useState([]);
  const [attractionsData, setAttractionsData] = useState([]);
  const [arrivalDate, setArrivalDate] = useState("");
  const [numDays, setNumDays] = useState(1);
 
  useEffect(() => {
    fetch("http://localhost:8000/places")
      .then((response) => response.json())
      .then((data) => {
        setAttractionsData(data);
      })
      .catch((error) => {
        console.error("Error loading places:", error);
      });
  }, []);
 
  const toggleCategory = (category) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(selectedCategories.filter((item) => item !== category));
    } else {
      setSelectedCategories([...selectedCategories, category]);
    }
  };
 
  const allSelected = selectedCategories.length === categories.length;

  const toggleAll = () => {
    if (allSelected) {
      setSelectedCategories([]);
    } else {
      setSelectedCategories(categories);
    }
  };
 
  const filteredAttractions =
    selectedCategories.length === 0
      ? attractionsData
      : attractionsData.filter((attraction) =>
          selectedCategories.includes(attraction.category)
        );
 
  const toggleAttraction = (attraction) => {
    const alreadySelected = selectedAttractions.some(
      (item) => item.id === attraction.id
    );
    if (alreadySelected) {
      setSelectedAttractions(
        selectedAttractions.filter((item) => item.id !== attraction.id)
      );
    } else {
      setSelectedAttractions([...selectedAttractions, attraction]);
    }
  };
 
  const totalMinutes = selectedAttractions.reduce(
    (sum, attraction) => sum + parseDurationToMinutes(attraction.duration),
    0
  );
  const totalDuration = formatMinutes(totalMinutes);
 
  const departureDate = arrivalDate
    ? new Date(new Date(arrivalDate).getTime() + numDays * 24 * 60 * 60 * 1000)
        .toISOString()
        .split("T")[0]
    : null; 
  return (
    <div className="app">
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
                <input
                  id="arrival"
                  type="date"
                  value={arrivalDate}
                  onChange={(e) => setArrivalDate(e.target.value)}
                />
              </div>
 
              <div className="stay-field">
                <label htmlFor="days">Number of days</label>
                <input
                  id="days"
                  type="number"
                  min="1"
                  max="30"
                  value={numDays}
                  onChange={(e) =>
                    setNumDays(Math.max(1, parseInt(e.target.value) || 1))
                  }
                />
              </div>
 
              {arrivalDate && (
                <div className="stay-summary">
                  {arrivalDate} → {departureDate} · {numDays}{" "}
                  {numDays === 1 ? "day" : "days"}
                </div>
              )}
            </div>
          </div>
 
          <div className="panel">
            <h2>Select Your Interests</h2>
            <p>Choose categories that match your travel style</p>
 
            <div className="categories">
              <button
                className={allSelected ? "category active" : "category"}
                onClick={toggleAll}
              >
                All
              </button>
              {categories.map((category) => (
                <button
                  key={category}
                  className={
                    selectedCategories.includes(category)
                      ? "category active"
                      : "category"
                  }
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
 
      {page === "results" && (
        <section className="results">
          <button className="back" onClick={() => setPage("home")}>
            ← Back to Categories
          </button>
 
          <div className="results-header">
            <div>
              <h1>Available Attractions</h1>
              <p>{selectedAttractions.length} attractions selected</p>
            </div>
 
            <button
              className="primary"
              disabled={selectedAttractions.length === 0}
              onClick={() => setPage("itinerary")}
            >
              Generate Itinerary
            </button>
          </div>
 
          <div className="filters">
            <button className="category active">All</button>
            {selectedCategories.map((category) => (
              <button key={category} className="category">
                {category}
              </button>
            ))}
          </div>
 
          <div className="cards">
            {filteredAttractions.map((attraction) => {
              const isSelected = selectedAttractions.some(
                (item) => item.id === attraction.id
              );
 
              return (
                <div
                  key={attraction.id}
                  className={isSelected ? "card selected" : "card"}
                >
                  <img src={attraction.image_url} alt={attraction.name_en} />
 
                  <div className="card-body">
                    <div className="tags">
                      <span>{attraction.category}</span>
                    </div>
 
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
        </section>
      )}
 
      {page === "itinerary" && (
        <section className="itinerary">
          <button className="back" onClick={() => setPage("results")}>
            ← Back to Attractions
          </button>
 
          <h1>Your Travel Itinerary</h1>
          {arrivalDate && (
            <p>
              {arrivalDate} → {departureDate} · {numDays}{" "}
              {numDays === 1 ? "day" : "days"}
            </p>
          )}
 
          <div className="total-duration">
            <span className="total-duration-label">Total duration</span>
            <span className="total-duration-value">{totalDuration}</span>
          </div>
 
          <div className="itinerary-list">
            {selectedAttractions.map((attraction, index) => (
              <div key={attraction.id} className="itinerary-item">
                <strong>
                  {index + 1}. {attraction.name_en || attraction.name_pl}
                </strong>
                <span>{attraction.duration}</span>
              </div>
            ))}
          </div>
 
          <button className="primary">Regenerate Itinerary</button>
        </section>
      )}
    </div>
  );
}
 
export default App;