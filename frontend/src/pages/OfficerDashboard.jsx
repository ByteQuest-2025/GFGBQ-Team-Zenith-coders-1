import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { officerAPI } from '../services/api';
import ComplaintInbox from '../components/officer/ComplaintInbox';
import ComplaintTracker from '../components/citizen/ComplaintTracker';
import UpdateStatusForm from '../components/officer/UpdateStatusForm';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { LogOut, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function OfficerDashboard() {
  const { user, logout } = useAuthStore();
  const [complaints, setComplaints] = useState([]);
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [complaintsRes, statsRes] = await Promise.all([
        officerAPI.getAssignedComplaints(),
        officerAPI.getStats(),
      ]);
      
      setComplaints(complaintsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to load officer data:', error);
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusUpdated = () => {
    loadData();
    if (selectedComplaint) {
      setSelectedComplaint(complaints.find(c => c.complaint_id === selectedComplaint.complaint_id));
    }
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
            <h1 className="text-2xl font-bold text-gray-900">Officer Dashboard</h1>
            <p className="text-sm text-gray-600">Welcome, {user?.name || user?.email}</p>
          </div>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* Stats Cards */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total Assigned</CardTitle>
              <AlertCircle className="h-4 w-4 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.total_assigned || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">In Progress</CardTitle>
              <Clock className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.in_progress || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Resolved</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.resolved || 0}</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Complaint Inbox */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Assigned Complaints</h2>
            {loading ? (
              <Card>
                <CardContent className="p-6">
                  <p className="text-center text-gray-500">Loading...</p>
                </CardContent>
              </Card>
            ) : (
              <ComplaintInbox
                complaints={complaints}
                selectedId={selectedComplaint?.complaint_id}
                onSelect={setSelectedComplaint}
              />
            )}
          </div>

          {/* Middle Column - Complaint Details */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Details</h2>
            {selectedComplaint ? (
              <ComplaintTracker complaintId={selectedComplaint.complaint_id} />
            ) : (
              <Card>
                <CardContent className="p-12 text-center">
                  <p className="text-gray-400">Select a complaint to view details</p>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Update Status */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-semibold mb-4">Actions</h2>
            {selectedComplaint ? (
              <UpdateStatusForm
                complaint={selectedComplaint}
                onSuccess={handleStatusUpdated}
              />
            ) : (
              <Card>
                <CardContent className="p-12 text-center">
                  <p className="text-gray-400">Select a complaint to update status</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
