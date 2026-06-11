function getAttractionName(attraction) {
  return attraction.name_en || attraction.name_pl || "Unnamed attraction";
}

function formatCategories(attraction) {
  if (Array.isArray(attraction.categories) && attraction.categories.length > 0) {
    return attraction.categories.join(", ");
  }

  return attraction.category || "Not specified";
}

function formatLocation(attraction) {
  return attraction.location || attraction.address || attraction.opening_hours || "Not available";
}

export default function AttractionDetailsModal({ attraction, onClose }) {
  if (!attraction) return null;

  const hasCoordinates = attraction.latitude != null && attraction.longitude != null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="details-modal" role="dialog" aria-modal="true" aria-labelledby="attraction-details-title" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose} aria-label="Close attraction details">
          x
        </button>

        {attraction.image_url && (
          <img className="details-image" src={attraction.image_url} alt={getAttractionName(attraction)} />
        )}

        <div className="details-body">
          <div className="tags"><span>{formatCategories(attraction)}</span></div>
          <h2 id="attraction-details-title">{getAttractionName(attraction)}</h2>
          <p>{attraction.description || "No description available."}</p>

          <dl className="details-list">
            <div>
              <dt>Estimated duration</dt>
              <dd>{attraction.duration || "Not specified"}</dd>
            </div>
            <div>
              <dt>Location</dt>
              <dd>{formatLocation(attraction)}</dd>
            </div>
            {hasCoordinates && (
              <div>
                <dt>Latitude / Longitude</dt>
                <dd>{attraction.latitude}, {attraction.longitude}</dd>
              </div>
            )}
          </dl>
        </div>
      </div>
    </div>
  );
}
