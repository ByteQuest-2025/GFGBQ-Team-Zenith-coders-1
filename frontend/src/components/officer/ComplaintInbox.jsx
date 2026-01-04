import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import StatusBadge from '../shared/StatusBadge';
import UrgencyBadge from '../shared/UrgencyBadge';
import CategoryBadge from '../shared/CategoryBadge';
import { Clock, MapPin, Calendar } from 'lucide-react';

export default function ComplaintInbox({ complaints, selectedId, onSelect }) {
  if (!complaints || complaints.length === 0) {
    return (
      <Card>
        <CardContent className="p-12 text-center">
          <p className="text-gray-500">No complaints assigned</p>
        </CardContent>
      </Card>
    );
  }

  const getTimeRemaining = (slaHours, createdAt) => {
    const created = new Date(createdAt);
    const deadline = new Date(created.getTime() + slaHours * 60 * 60 * 1000);
    const now = new Date();
    const diff = deadline - now;
    
    if (diff < 0) return { text: 'Overdue', color: 'text-red-600' };
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours < 2) return { text: `${hours}h ${minutes}m`, color: 'text-red-600' };
    if (hours < 6) return { text: `${hours}h ${minutes}m`, color: 'text-yellow-600' };
    return { text: `${hours}h ${minutes}m`, color: 'text-green-600' };
  };

  return (
    <div className="space-y-3">
      {complaints.map((complaint) => {
        const timeRemaining = getTimeRemaining(
          complaint.routing?.sla_hours || 24,
          complaint.created_at
        );
        
        return (
          <Card
            key={complaint.complaint_id}
            className={`cursor-pointer hover:shadow-md transition-shadow ${
              selectedId === complaint.complaint_id ? 'border-blue-500 border-2' : ''
            }`}
            onClick={() => onSelect(complaint)}
          >
            <CardHeader className="pb-3">
              <div className="flex justify-between items-start gap-2">
                <CardTitle className="text-base flex-1">{complaint.title}</CardTitle>
                <div className="flex flex-col gap-1 items-end">
                  <StatusBadge status={complaint.status} />
                  <UrgencyBadge level={complaint.urgency_level} />
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <CategoryBadge category={complaint.category} />
                <Badge variant="outline" className={timeRemaining.color}>
                  <Clock className="w-3 h-3 mr-1" />
                  {timeRemaining.text}
                </Badge>
              </div>
              
              <div className="flex items-start gap-2 text-xs text-gray-600">
                <MapPin className="w-3 h-3 mt-0.5 flex-shrink-0" />
                <span className="line-clamp-1">{complaint.location?.address}</span>
              </div>
              
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Calendar className="w-3 h-3" />
                <span>{new Date(complaint.created_at).toLocaleString()}</span>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
