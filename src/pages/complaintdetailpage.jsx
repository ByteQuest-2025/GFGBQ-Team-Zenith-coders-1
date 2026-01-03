import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronRight, MapPin, RefreshCw, FileImage, Mic, ExternalLink } from 'lucide-react';
import { mockComplaints } from '../data/mockdata';
import { useToast } from '../context/toastcontext';
import Card from '../components/ui/card';
import Button from '../components/ui/button';
import Badge from '../components/ui/badge';
import StatusBadge from '../components/ui/statusbadge';
import UrgencyBadge from '../components/ui/urgencybadge';
import Timeline from '../components/ui/timeline';
import Spinner from '../components/ui/spinner';
import EmptyState from '../components/ui/emptystate';

const ComplaintDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Mock fetch - replace with actual API call
    const found = mockComplaints.find(c => c.id === id || c.complaint_id === id);
    setTimeout(() => {
      setComplaint(found || mockComplaints[0]);
      setLoading(false);
    }, 500);
    
    // Poll for updates every 10 seconds until resolved
    const interval = setInterval(() => {
      if (complaint && complaint.status !== 'RESOLVED') {
        // Fetch updated status
        console.log('Polling for updates...');
      }
    }, 10000);
    
    return () => clearInterval(interval);
  }, [id, complaint]);
  
  const handleRefresh = () => {
    setLoading(true);
    setTimeout(() => {
      showToast('Status refreshed', 'info');
      setLoading(false);
    }, 1000);
  };
  
  if (loading) return <Spinner />;
  if (!complaint) return <EmptyState title="Complaint not found" description="This complaint does not exist" />;
  
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="mb-6">
        <button onClick={() => navigate('/my')} className="text-blue-600 hover:text-blue-700 flex items-center gap-2 mb-4">
          <ChevronRight size={20} className="rotate-180" />
          Back to My Complaints
        </button>
        
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-3xl font-bold mb-2">{complaint.title}</h1>
            <div className="flex items-center gap-3 flex-wrap">
              <span className="font-mono text-gray-600">{complaint.complaint_id}</span>
              <StatusBadge status={complaint.status} />
              {complaint.urgency_level && (
                <UrgencyBadge level={complaint.urgency_level} score={complaint.urgency_score} />
              )}
            </div>
          </div>
          
          <Button variant="outline" size="sm" onClick={handleRefresh}>
            <RefreshCw size={16} />
            Refresh Status
          </Button>
        </div>
      </div>
      
      <div className="grid md:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="md:col-span-2 space-y-6">
          <Card>
            <h2 className="font-bold text-xl mb-4">Complaint Details</h2>
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">Description</label>
                <p className="mt-1 text-gray-900">{complaint.description}</p>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600">Category</label>
                  <div className="mt-1 flex items-center gap-2">
                    <span className="font-semibold">{complaint.category}</span>
                    {complaint.category_confidence && (
                      <Badge variant="info">{Math.round(complaint.category_confidence * 100)}% confidence</Badge>
                    )}
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-600">Submitted On</label>
                  <p className="mt-1 font-semibold">{new Date(complaint.created_at).toLocaleDateString()}</p>
                </div>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-600">Location</label>
                <div className="mt-1 flex items-start gap-2">
                  <MapPin size={16} className="text-gray-500 mt-1" />
                  <span className="font-semibold">{complaint.location.address}</span>
                </div>
              </div>
              
              {complaint.attachments && complaint.attachments.length > 0 && (
                <div>
                  <label className="text-sm font-medium text-gray-600 block mb-2">Attachments</label>
                  <div className="grid grid-cols-2 gap-4">
                    {complaint.attachments.map((att, idx) => (
                      <div key={idx} className="border rounded-lg p-4">
                        {att.type === 'image' ? (
                          <FileImage className="text-gray-400 mb-2" />
                        ) : (
                          <Mic className="text-gray-400 mb-2" />
                        )}
                        <a href={att.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 text-sm flex items-center gap-1">
                          View {att.type}
                          <ExternalLink size={14} />
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Card>
          
          <Card>
            <h2 className="font-bold text-xl mb-4">Status Timeline</h2>
            <Timeline items={complaint.status_history} />
          </Card>
        </div>
        
        {/* Sidebar */}
        <div className="space-y-6">
          <Card>
            <h3 className="font-bold text-lg mb-4">Assignment Info</h3>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-600">Department</label>
                <p className="mt-1 font-semibold">{complaint.assigned_department || 'Pending'}</p>
              </div>
              
              {complaint.assigned_officer && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Assigned Officer</label>
                  <p className="mt-1 font-semibold">{complaint.assigned_officer.name}</p>
                </div>
              )}
            </div>
          </Card>
          
          {complaint.urgency_level && (
            <Card>
              <h3 className="font-bold text-lg mb-4">AI Analysis</h3>
              <div className="space-y-3">
                <div>
                  <label className="text-sm font-medium text-gray-600">Urgency Assessment</label>
                  <div className="mt-2">
                    <UrgencyBadge level={complaint.urgency_level} score={complaint.urgency_score} />
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium text-gray-600">Why this urgency?</label>
                  <div className="mt-2 flex flex-wrap gap-2">
                    <Badge variant="default">Public safety</Badge>
                    <Badge variant="default">High impact</Badge>
                  </div>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default ComplaintDetailPage;