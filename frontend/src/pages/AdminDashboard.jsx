import { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { adminAPI, complaintAPI } from '../services/api';
import AnalyticsCharts from '../components/admin/AnalyticsCharts';
import OfficerManagement from '../components/admin/OfficerManagement';
import ComplaintHeatmap from '../components/admin/ComplaintHeatmap';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { LogOut, BarChart3, Users, Map } from 'lucide-react';
import toast from 'react-hot-toast';

export default function AdminDashboard() {
  const { user, logout } = useAuthStore();
  const [analytics, setAnalytics] = useState(null);
  const [officers, setOfficers] = useState([]);
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [analyticsRes, officersRes, complaintsRes] = await Promise.all([
        adminAPI.getAnalytics(),
        adminAPI.getAllOfficers(),
        complaintAPI.getAll(),
      ]);
      
      setAnalytics(analyticsRes.data);
      setOfficers(officersRes.data);
      setComplaints(complaintsRes.data);
    } catch (error) {
      console.error('Failed to load admin data:', error);
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
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
            <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-sm text-gray-600">Welcome, {user?.name || user?.email}</p>
          </div>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </div>
      </header>

      {/* Stats Overview */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Complaints</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analytics?.total_complaints || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Active Officers</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{officers?.length || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Avg Resolution Time</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {analytics?.avg_resolution_time 
                  ? `${analytics.avg_resolution_time}h` 
                  : 'N/A'}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Pending Complaints</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{analytics?.pending_count || 0}</div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Main Content - Tabs */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        {loading ? (
          <Card>
            <CardContent className="p-12 text-center">
              <p className="text-gray-500">Loading dashboard...</p>
            </CardContent>
          </Card>
        ) : (
          <Tabs defaultValue="analytics" className="space-y-4">
            <TabsList>
              <TabsTrigger value="analytics">
                <BarChart3 className="w-4 h-4 mr-2" />
                Analytics
              </TabsTrigger>
              <TabsTrigger value="officers">
                <Users className="w-4 h-4 mr-2" />
                Officers
              </TabsTrigger>
              <TabsTrigger value="map">
                <Map className="w-4 h-4 mr-2" />
                Heatmap
              </TabsTrigger>
            </TabsList>

            <TabsContent value="analytics">
              <AnalyticsCharts analytics={analytics} />
            </TabsContent>

            <TabsContent value="officers">
              <OfficerManagement
                officers={officers}
                complaints={complaints}
                onReassign={loadData}
              />
            </TabsContent>

            <TabsContent value="map">
              <ComplaintHeatmap complaints={complaints} />
            </TabsContent>
          </Tabs>
        )}
      </main>
    </div>
  );
}
