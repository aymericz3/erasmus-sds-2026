import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import { POZNAN_CENTER, DAY_COLORS } from "../constants";
import { createMarkerIcon } from "../utils";

export default function ItineraryMap({ days }) {
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
