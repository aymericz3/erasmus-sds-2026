import { CATEGORIES } from "../constants";
import ResultsMap from "./ResultsMap";

export default function ResultsPage({
  attractions, selectedAttractions, selectedCategories, allCategoriesSelected,
  onToggleAttraction, onToggleCategory, onToggleAllCategories,
  onBack, onGenerateItinerary,
}) {
  return (
    <section className="results">
      <button className="back" onClick={onBack}>← Back to Categories</button>

      <div className="results-header">
        <div>
          <h1>Available Attractions</h1>
          <p>{selectedAttractions.length} attractions selected</p>
        </div>
        <button
          className="primary"
          disabled={selectedAttractions.length === 0}
          onClick={onGenerateItinerary}
        >
          Generate Itinerary
        </button>
      </div>

      <div className="filters">
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

      <div className="results-layout">
        <div className="cards">
          {attractions.map((attraction) => {
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
                    onClick={() => onToggleAttraction(attraction)}
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
            attractions={attractions}
            selectedAttractions={selectedAttractions}
            onToggle={onToggleAttraction}
          />
        </div>
      </div>
    </section>
  );
}
