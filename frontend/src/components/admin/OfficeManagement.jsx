import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Button } from '../ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { User, Mail, Phone, MapPin } from 'lucide-react';
import { adminAPI } from '../../services/api';
import toast from 'react-hot-toast';

export default function OfficerManagement({ officers, complaints, onReassign }) {
  const [selectedComplaint, setSelectedComplaint] = useState('');
  const [selectedOfficer, setSelectedOfficer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleReassign = async () => {
    if (!selectedComplaint || !selectedOfficer) {
      toast.error('Please select both complaint and officer');
      return;
    }

    setLoading(true);
    try {
      await adminAPI.reassignComplaint(selectedComplaint, selectedOfficer);
      toast.success('Complaint reassigned successfully');
      setSelectedComplaint('');
      setSelectedOfficer('');
      onReassign?.();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to reassign complaint');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Officers List */}
      <Card>
        <CardHeader>
          <CardTitle>Officers</CardTitle>
        </CardHeader>
        <CardContent>
          {!officers || officers.length === 0 ? (
            <p className="text-center text-gray-500 py-4">No officers found</p>
          ) : (
            <div className="space-y-3">
              {officers.map((officer) => (
                <div
                  key={officer.officer_id}
                  className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex justify-between items-start">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-gray-500" />
                        <p className="font-medium">{officer.name}</p>
                        <Badge variant="outline">{officer.department}</Badge>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Mail className="w-3 h-3" />
                        <span>{officer.email}</span>
                      </div>
                      {officer.phone && (
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <Phone className="w-3 h-3" />
                          <span>{officer.phone}</span>
                        </div>
                      )}
                      {officer.zone && (
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <MapPin className="w-3 h-3" />
                          <span>Zone: {officer.zone}</span>
                        </div>
                      )}
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-600">Assigned</p>
                      <p className="text-2xl font-bold">{officer.assigned_count || 0}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Reassignment Tool */}
      <Card>
        <CardHeader>
          <CardTitle>Reassign Complaint</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">Select Complaint</label>
            <Select value={selectedComplaint} onValueChange={setSelectedComplaint}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a complaint" />
              </SelectTrigger>
              <SelectContent>
                {complaints?.map((complaint) => (
                  <SelectItem key={complaint.complaint_id} value={complaint.complaint_id}>
                    {complaint.title} - {complaint.category}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-sm font-medium mb-2 block">Select New Officer</label>
            <Select value={selectedOfficer} onValueChange={setSelectedOfficer}>
              <SelectTrigger>
                <SelectValue placeholder="Choose an officer" />
              </SelectTrigger>
              <SelectContent>
                {officers?.map((officer) => (
                  <SelectItem key={officer.officer_id} value={officer.officer_id}>
                    {officer.name} - {officer.department} ({officer.assigned_count || 0} assigned)
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <Button
            onClick={handleReassign}
            disabled={loading || !selectedComplaint || !selectedOfficer}
            className="w-full"
          >
            {loading ? 'Reassigning...' : 'Reassign Complaint'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
