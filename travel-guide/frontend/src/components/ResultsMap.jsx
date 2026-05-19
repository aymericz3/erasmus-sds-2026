import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { POZNAN_CENTER } from "../constants";
import { createMarkerIcon } from "../utils";

export default function ResultsMap({ attractions, selectedAttractions, onToggle }) {
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
