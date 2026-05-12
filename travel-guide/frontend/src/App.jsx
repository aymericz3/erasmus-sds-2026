import { useState, useEffect } from "react";

const categories = [
  "Culture",
  "Art",
  "Sports",
  "Nature",
  "History",
  "Family",
  "Food",
  "Architecture",
];

const categoryMap = {
  landmark: "History",
  sport: "Sports",
  culture: "Culture",
  outdoor: "Nature",
  family: "Family",
  food: "Food",
  art: "Art",
  hotel: "Architecture"
};

function App() {
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [page, setPage] = useState("home");
  const [selectedAttractions, setSelectedAttractions] = useState([]);
  const [attractions, setAttractions] = useState([]);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL;
    
    fetch(`${apiUrl}/places`)
      .then((response) => response.json())
      .then((data) => {
        const formattedData = data.map((item) => ({
          id: item.id,
          name: item.name_en || item.name_pl,
          description: item.description,
          categories: [categoryMap[item.category] || "Culture"],
          duration: item.duration || "1h",
          location: "City Center",
          image: item.image_url,
        }));
        setAttractions(formattedData);
      })
      .catch((error) => console.error(error));
}, []);

  const toggleCategory = (category) => {
    if (selectedCategories.includes(category)) {
      setSelectedCategories(selectedCategories.filter((item) => item !== category));
    } else {
      setSelectedCategories([...selectedCategories, category]);
    }
  };

  const selectAllCategories = () => {
    setSelectedCategories(categories);
  };

  const filteredAttractions =
    selectedCategories.length === 0
      ? attractions
      : attractions.filter((attraction) =>
          attraction.categories.some((category) =>
            selectedCategories.includes(category)
          )
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
            <h2>Select Your Interests</h2>
            <p>Choose categories that match your travel style</p>

            <div className="categories">
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
              <button className="secondary" onClick={selectAllCategories}>
                Select All
              </button>

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
                  <img src={attraction.image} alt={attraction.name} />

                  <div className="card-body">
                    <div className="tags">
                      {attraction.categories.map((category) => (
                        <span key={category}>{category}</span>
                      ))}
                    </div>

                    <h3>{attraction.name}</h3>
                    <p>{attraction.description}</p>

                    <div className="info">
                      <span>{attraction.duration}</span>
                      <span>{attraction.location}</span>
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
          <p>This is your selected visit plan for Poznań.</p>

          <div className="itinerary-list">
            {selectedAttractions.map((attraction, index) => (
              <div key={attraction.id} className="itinerary-item">
                <strong>
                  {index + 1}. {attraction.name}
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