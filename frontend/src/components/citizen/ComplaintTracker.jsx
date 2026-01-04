import { useEffect, useState } from 'react';
import { complaintAPI } from '../../services/api';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import StatusBadge from '../shared/StatusBadge';
import UrgencyBadge from '../shared/UrgencyBadge';
import CategoryBadge from '../shared/CategoryBadge';
import FeedbackForm from './FeedbackForm';
import { Clock, MapPin, Tag, TrendingUp, User, AlertTriangle } from 'lucide-react';

export default function ComplaintTracker({ complaintId }) {
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    loadComplaint();
    const interval = setInterval(loadComplaint, 10000);
    return () => clearInterval(interval);
  }, [complaintId]);
  
  const loadComplaint = async () => {
    try {
      const response = await complaintAPI.getById(complaintId);
      setComplaint(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) {
    return (
      <Card>
        <CardContent className="p-12">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }
  
  if (!complaint) {
    return (
      <Card>
        <CardContent className="p-12">
          <p className="text-center text-gray-500">Complaint not found</p>
        </CardContent>
      </Card>
    );
  }
  
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-lg">{complaint.title}</CardTitle>
              <p className="text-sm text-gray-500 mt-1">{complaint.complaint_id}</p>
            </div>
            <StatusBadge status={complaint.status} />
          </div>
        </CardHeader>
        
        <CardContent className="space-y-4">
          <div>
            <p className="text-sm text-gray-700">{complaint.description}</p>
          </div>
          
          {/* Duplicate Warning */}
          {complaint.duplicate_check?.is_duplicate && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-yellow-900">
                    Similar Complaints Detected
                  </p>
                  <p className="text-xs text-yellow-700 mt-1">
                    We found {complaint.duplicate_check.duplicate_count} similar complaint(s). 
                    Your issue may already be addressed.
                  </p>
                  {complaint.duplicate_check.similar_complaints?.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {complaint.duplicate_check.similar_complaints.slice(0, 2).map((dup, idx) => (
                        <div key={idx} className="text-xs bg-white p-2 rounded border border-yellow-200">
                          <p className="font-medium">{dup.complaint_id}</p>
                          <p className="text-gray-600">{dup.title}</p>
                          <p className="text-gray-500">Status: {dup.status}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
          
          {/* AI Analysis Section */}
          {complaint.triage && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded-lg space-y-3 border border-blue-200">
              <h3 className="font-semibold text-sm flex items-center gap-2">
                <Tag className="w-4 h-4 text-blue-600" />
                AI Analysis Results
              </h3>
              
              <div className="flex flex-wrap gap-2">
                <CategoryBadge category={complaint.triage.category} />
                <UrgencyBadge level={complaint.triage.urgency_level} />
                {complaint.triage.category_confidence && (
                  <Badge variant="outline" className="bg-white">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    {(complaint.triage.category_confidence * 100).toFixed(0)}% Confidence
                  </Badge>
                )}
              </div>
              
              {complaint.triage.keywords_detected?.length > 0 && (
                <div className="mt-3">
                  <p className="text-xs text-gray-600 mb-2">Detected Keywords:</p>
                  <div className="flex flex-wrap gap-1">
                    {complaint.triage.keywords_detected.slice(0, 8).map((kw, idx) => (
                      <span key={idx} className="text-xs bg-white px-2 py-1 rounded border border-blue-200">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
          {/* Assignment Info */}
          {complaint.routing?.assigned_officer_name && (
            <div className="bg-green-50 p-4 rounded-lg border border-green-200">
              <h3 className="font-semibold text-sm mb-2 text-green-900 flex items-center gap-2">
                <User className="w-4 h-4" />
                Assignment Details
              </h3>
              <div className="space-y-1 text-sm text-green-800">
                <p><strong>Officer:</strong> {complaint.routing.assigned_officer_name}</p>
                <p><strong>Department:</strong> {complaint.routing.assigned_department}</p>
                <p className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  <strong>SLA:</strong> {complaint.routing.sla_hours} hours
                </p>
              </div>
            </div>
          )}
          
          {/* Location */}
          <div className="flex items-start gap-2 text-sm">
            <MapPin className="w-4 h-4 mt-1 text-gray-400" />
            <p className="text-gray-600">{complaint.location.address}</p>
          </div>
          
          {/* Status History */}
          <div>
            <h3 className="font-semibold text-sm mb-3">Status Timeline</h3>
            <div className="space-y-3">
              {complaint.status_history?.map((entry, idx) => (
                <div key={idx} className="flex gap-3">
                  <div className="flex flex-col items-center">
                    <div className={`w-3 h-3 rounded-full ${
                      idx === 0 ? 'bg-blue-500' : 'bg-gray-300'
                    }`} />
                    {idx < complaint.status_history.length - 1 && (
                      <div className="w-0.5 h-full bg-gray-200 my-1" />
                    )}
                  </div>
                  <div className="flex-1 pb-4">
                    <div className="flex items-center gap-2 mb-1">
                      <StatusBadge status={entry.status} />
                      <span className="text-xs text-gray-400">
                        {new Date(entry.timestamp).toLocaleString()}
                      </span>
                    </div>
                    {entry.note && (
                      <p className="text-sm text-gray-600">{entry.note}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
      
      {/* Feedback Form */}
      {complaint.status === 'RESOLVED' && (
        <FeedbackForm complaint={complaint} onSuccess={loadComplaint} />
      )}
    </div>
  );
}
