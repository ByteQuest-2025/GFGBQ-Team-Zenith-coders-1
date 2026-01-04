import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const CATEGORY_COLORS = {
  Infrastructure: '#9333ea',
  Sanitation: '#22c55e',
  Utilities: '#3b82f6',
  Safety: '#ef4444',
  Health: '#ec4899',
  Administrative: '#6b7280',
};

const URGENCY_COLORS = {
  HIGH: '#ef4444',
  MEDIUM: '#f59e0b',
  LOW: '#22c55e',
};

export default function AnalyticsCharts({ analytics }) {
  if (!analytics) {
    return (
      <Card>
        <CardContent className="p-12 text-center">
          <p className="text-gray-500">No analytics data available</p>
        </CardContent>
      </Card>
    );
  }

  const categoryData = analytics.by_category ? Object.entries(analytics.by_category).map(([name, value]) => ({
    name,
    value,
    fill: CATEGORY_COLORS[name] || '#6b7280'
  })) : [];

  const urgencyData = analytics.by_urgency ? Object.entries(analytics.by_urgency).map(([name, value]) => ({
    name,
    value,
    fill: URGENCY_COLORS[name] || '#6b7280'
  })) : [];

  const statusData = analytics.by_status ? Object.entries(analytics.by_status).map(([name, value]) => ({
    name: name.replace('_', ' '),
    value
  })) : [];

  const resolutionTrend = analytics.resolution_trend || [];

  return (
    <div className="space-y-6">
      {/* Category Distribution */}
      <Card>
        <CardHeader>
          <CardTitle>Complaints by Category</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={(entry) => `${entry.name}: ${entry.value}`}
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Urgency Distribution */}
      <Card>
        <CardHeader>
          <CardTitle>Complaints by Urgency Level</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={urgencyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6">
                {urgencyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Status Distribution */}
      <Card>
        <CardHeader>
          <CardTitle>Complaints by Status</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Resolution Trend */}
      {resolutionTrend.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Resolution Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={resolutionTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="resolved" stroke="#22c55e" name="Resolved" />
                <Line type="monotone" dataKey="submitted" stroke="#3b82f6" name="Submitted" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
