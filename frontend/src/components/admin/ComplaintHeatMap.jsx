import { useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import StatusBadge from '../shared/StatusBadge';
import CategoryBadge from '../shared/CategoryBadge';

const getMarkerColor = (urgencyLevel) => {
  switch (urgencyLevel) {
    case 'HIGH':
      return '#ef4444';
    case 'MEDIUM':
      return '#f59e0b';
    case 'LOW':
      return '#22c55e';
    default:
      return '#6b7280';
  }
};

export default function ComplaintHeatmap({ complaints }) {
  const mapRef = useRef(null);

  const complaintsWithLocation = complaints?.filter(
    (c) => c.location?.latitude && c.location?.longitude
  ) || [];

  const center = complaintsWithLocation.length > 0
    ? [complaintsWithLocation[0].location.latitude, complaintsWithLocation[0].location.longitude]
    : [13.0827, 80.2707]; // Default to Chennai

  useEffect(() => {
    // Fix Leaflet icon issue in React
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    });
  }, []);

  if (complaintsWithLocation.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Complaint Heatmap</CardTitle>
        </CardHeader>
        <CardContent className="p-12 text-center">
          <p className="text-gray-500">No complaints with location data available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Complaint Heatmap</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-96 rounded-lg overflow-hidden">
          <MapContainer
            center={center}
            zoom={12}
            style={{ height: '100%', width: '100%' }}
            ref={mapRef}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {complaintsWithLocation.map((complaint) => (
              <CircleMarker
                key={complaint.complaint_id}
                center={[complaint.location.latitude, complaint.location.longitude]}
                radius={8}
                fillColor={getMarkerColor(complaint.urgency_level)}
                color="#fff"
                weight={2}
                opacity={1}
                fillOpacity={0.8}
              >
                <Popup>
                  <div className="space-y-2 p-2">
                    <p className="font-semibold">{complaint.title}</p>
                    <div className="flex gap-2">
                      <CategoryBadge category={complaint.category} />
                      <StatusBadge status={complaint.status} />
                    </div>
                    <p className="text-xs text-gray-600">{complaint.location.address}</p>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
        
        <div className="mt-4 flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span>High Urgency</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span>Medium Urgency</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span>Low Urgency</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
