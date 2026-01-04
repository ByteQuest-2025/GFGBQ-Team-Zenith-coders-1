import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { complaintAPI } from '../services/api';
import ComplaintForm from '../components/citizen/ComplaintForm';
import ComplaintTracker from '../components/citizen/ComplaintTracker';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { LogOut, Plus, FileText } from 'lucide-react';
import toast from 'react-hot-toast';

export default function CitizenDashboard() {
  const { user, logout } = useAuthStore();
  const [showForm, setShowForm] = useState(false);
  const [complaints, setComplaints] = useState([]);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadComplaints();
  }, []);

  const loadComplaints = async () => {
    try {
      const response = await complaintAPI.getAll({ mine: true });
      setComplaints(response.data);
    } catch (error) {
      console.error('Failed to load complaints:', error);
      toast.error('Failed to load complaints');
    } finally {
      setLoading(false);
    }
  };

  const handleComplaintSubmitted = (newComplaint) => {
    setShowForm(false);
    loadComplaints();
    setSelectedComplaint(newComplaint.complaint_id);
    toast.success('✅ Complaint submitted! AI is analyzing...');
  };

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">🏛️ Citizen Dashboard</h1>
            <p className="text-sm text-gray-600">Welcome, {user?.name || user?.email}</p>
          </div>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Form or Complaints List */}
          <div>
            {!showForm ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h2 className="text-xl font-semibold flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    My Complaints
                  </h2>
                  <Button onClick={() => setShowForm(true)}>
                    <Plus className="mr-2 h-4 w-4" />
                    New Complaint
                  </Button>
                </div>

                {loading ? (
                  <Card>
                    <CardContent className="p-6">
                      <p className="text-center text-gray-500">Loading complaints...</p>
                    </CardContent>
                  </Card>
                ) : complaints.length === 0 ? (
                  <Card>
                    <CardContent className="p-12 text-center">
                      <FileText className="w-12 h-12 mx-auto text-gray-300 mb-3" />
                      <p className="text-gray-500">No complaints yet.</p>
                      <p className="text-sm text-gray-400 mt-1">Submit your first complaint to get started!</p>
                    </CardContent>
                  </Card>
                ) : (
                  <div className="space-y-3">
                    {complaints.map((complaint) => (
                      <Card
                        key={complaint.complaint_id}
                        className={`cursor-pointer hover:shadow-md transition-shadow ${
                          selectedComplaint === complaint.complaint_id ? 'border-blue-500 border-2' : ''
                        }`}
                        onClick={() => setSelectedComplaint(complaint.complaint_id)}
                      >
                        <CardHeader className="pb-3">
                          <div className="flex justify-between items-start">
                            <CardTitle className="text-base">{complaint.title}</CardTitle>
                            <span className={`text-xs px-2 py-1 rounded font-medium ${
                              complaint.urgency_level === 'HIGH' ? 'bg-red-100 text-red-800' :
                              complaint.urgency_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-green-100 text-green-800'
                            }`}>
                              {complaint.urgency_level || 'LOW'}
                            </span>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-600">{complaint.category || 'Processing...'}</span>
                            <span className="text-gray-500">{complaint.status}</span>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <Button variant="outline" onClick={() => setShowForm(false)}>
                  ← Back to Complaints
                </Button>
                <ComplaintForm onSuccess={handleComplaintSubmitted} />
              </div>
            )}
          </div>

          {/* Right Column - Complaint Details */}
          <div>
            {selectedComplaint ? (
              <ComplaintTracker complaintId={selectedComplaint} />
            ) : (
              <Card>
                <CardContent className="p-12 text-center">
                  <FileText className="w-16 h-16 mx-auto text-gray-200 mb-4" />
                  <p className="text-gray-400 text-lg font-medium">
                    Select a complaint to view details
                  </p>
                  <p className="text-sm text-gray-400 mt-2">
                    AI analysis and status tracking will appear here
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
