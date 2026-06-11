import { CATEGORIES } from "../constants";
import ErrorMessage from "../components/ErrorMessage";
import LoadingMessage from "../components/LoadingMessage";
import ResultsMap from "../components/ResultsMap";

function getAttractionName(attraction) {
  return attraction.name_en || attraction.name_pl || "Unnamed attraction";
}

export default function ResultsPage({
  attractions, selectedAttractions, selectedCategories, allCategoriesSelected,
  isLoadingAttractions, attractionsError,
  onRetryAttractions, onToggleAttraction, onToggleCategory, onToggleAllCategories,
  onShowAttractionDetails, onBack, onGenerateItinerary,
}) {
  const hasAttractions = !isLoadingAttractions && !attractionsError && attractions.length > 0;

  return (
    <section className="results">
      <button className="back" onClick={onBack}>Back to Categories</button>

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
        <div className={hasAttractions ? "cards" : "cards cards-status"}>
          {isLoadingAttractions && <LoadingMessage message="Loading attractions..." />}

          {attractionsError && (
            <ErrorMessage
              message={attractionsError}
              onRetry={onRetryAttractions}
            />
          )}

          {!isLoadingAttractions && !attractionsError && attractions.length === 0 && (
            <div className="status-message empty-message">No attractions found.</div>
          )}

          {hasAttractions && attractions.map((attraction) => {
            const isSelected = selectedAttractions.some((a) => a.id === attraction.id);
            return (
              <div
                key={attraction.id}
                className={isSelected ? "card selected card-clickable" : "card card-clickable"}
                onClick={() => onShowAttractionDetails(attraction)}
              >
                {attraction.image_url ? (
                  <img src={attraction.image_url} alt={getAttractionName(attraction)} />
                ) : (
                  <div className="card-image-placeholder">No image available</div>
                )}
                <div className="card-body">
                  <div className="tags"><span>{attraction.category}</span></div>
                  <h3>{getAttractionName(attraction)}</h3>
                  <p>{attraction.description}</p>
                  <div className="info">
                    <span>{attraction.duration}</span>
                    <span>{attraction.price_range}</span>
                  </div>
                  <div className="card-actions">
                    <button
                      className="details-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        onShowAttractionDetails(attraction);
                      }}
                    >
                      Details
                    </button>
                    <button
                      className={isSelected ? "selected-btn" : "select-btn"}
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleAttraction(attraction);
                      }}
                    >
                      {isSelected ? "Selected" : "Select"}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {hasAttractions && (
          <div className="results-map-panel">
            <ResultsMap
              attractions={attractions}
              selectedAttractions={selectedAttractions}
              onToggle={onToggleAttraction}
            />
          </div>
        )}
      </div>
    </section>
  );
}
