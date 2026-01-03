import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, MapPin, ChevronRight } from 'lucide-react';
import { mockComplaints } from '../data/mockdata';
import Card from '../components/ui/card';
import Button from '../components/ui/button';
import Badge from '../components/ui/badge';
import StatusBadge from '../components/ui/statusbadge';
import UrgencyBadge from '../components/ui/urgencybadge';
import Spinner from '../components/ui/spinner';
import EmptyState from '../components/ui/emptystate';

const MyComplaintsPage = () => {
  const navigate = useNavigate();
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');
  
  useEffect(() => {
    // Mock fetch - replace with actual API call
    setTimeout(() => {
      setComplaints(mockComplaints);
      setLoading(false);
    }, 500);
  }, []);
  
  const filteredComplaints = complaints.filter(c => {
    const matchesFilter = filter === 'all' || c.status === filter;
    const matchesSearch = c.title.toLowerCase().includes(search.toLowerCase()) || 
                         c.complaint_id.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });
  
  if (loading) return <Spinner />;
  
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">My Complaints</h1>
        <p className="text-gray-600">Track and manage all your submitted complaints</p>
      </div>
      
      {/* Filters */}
      <Card className="mb-6">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search by title or ID..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
          
          <div className="flex gap-2 flex-wrap">
            {['all', 'SUBMITTED', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED'].map(status => (
              <button
                key={status}
                onClick={() => setFilter(status)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === status 
                    ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status === 'all' ? 'All' : status.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </Card>
      
      {/* Complaints List */}
      {filteredComplaints.length === 0 ? (
        <EmptyState
          title="No complaints found"
          description={search ? "Try adjusting your search" : "Submit your first complaint to get started"}
          action={!search && (
            <Button onClick={() => navigate('/submit')}>
              Submit Complaint
            </Button>
          )}
        />
      ) : (
        <div className="space-y-4">
          {filteredComplaints.map(complaint => (
            <Card 
              key={complaint.id} 
              hover 
              onClick={() => navigate(`/complaints/${complaint.id}`)}
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2 flex-wrap">
                    <span className="font-mono text-sm text-gray-500">{complaint.complaint_id}</span>
                    <StatusBadge status={complaint.status} />
                    {complaint.urgency_level && (
                      <UrgencyBadge level={complaint.urgency_level} score={complaint.urgency_score} />
                    )}
                  </div>
                  <h3 className="text-xl font-semibold mb-1">{complaint.title}</h3>
                  <p className="text-gray-600 text-sm mb-2">{complaint.description.substring(0, 100)}...</p>
                  <div className="flex items-center gap-4 text-sm text-gray-500 flex-wrap">
                    <span className="flex items-center gap-1">
                      <MapPin size={14} />
                      {complaint.location.address}
                    </span>
                    <span>{new Date(complaint.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-2">
                  {complaint.category && (
                    <Badge variant="info">{complaint.category}</Badge>
                  )}
                  {complaint.assigned_department && (
                    <span className="text-sm text-gray-600">📍 {complaint.assigned_department}</span>
                  )}
                  <ChevronRight className="text-gray-400" />
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyComplaintsPage;