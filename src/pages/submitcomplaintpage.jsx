import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin } from 'lucide-react';
import { useToast } from '../context/toastcontext';
import { generateComplaintId } from '../lib/utils';
import Card from '../components/ui/card';
import Input from '../components/ui/input';
import Textarea from '../components/ui/textarea';
import Select from '../components/ui/select';
import Button from '../components/ui/button';
import FileUpload from '../components/ui/fileupload';

const SubmitComplaintPage = () => {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'auto',
    address: '',
    language: 'auto'
  });
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState('');
  const [audioFile, setAudioFile] = useState(null);
  const [location, setLocation] = useState(null);
  
  const handleImageChange = (file) => {
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
  };
  
  const handleAudioChange = (file) => {
    setAudioFile(file);
  };
  
  const handleUseLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
          showToast('Location captured successfully', 'success');
        },
        () => {
          showToast('Unable to get location', 'error');
        }
      );
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Mock submission - replace with actual API call
      const complaintId = generateComplaintId();
      
      setTimeout(() => {
        showToast('Complaint submitted successfully!', 'success');
        navigate(`/complaints/${complaintId}`);
        setLoading(false);
      }, 1500);
    } catch (error) {
      showToast('Submission failed. Please try again.', 'error');
      setLoading(false);
    }
  };
  
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Submit a Complaint</h1>
        <p className="text-gray-600">Our AI will automatically categorize and prioritize your complaint</p>
      </div>
      
      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Complaint Title *"
            type="text"
            placeholder="Brief description of the issue"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            required
          />
          
          <Textarea
            label="Detailed Description *"
            placeholder="Provide detailed information about your complaint"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            required
          />
          
          <Select
            label="Category"
            options={[
              { value: 'auto', label: 'Auto-detect by AI' },
              { value: 'utilities', label: 'Utilities' },
              { value: 'roads', label: 'Roads & Transport' },
              { value: 'water', label: 'Water Supply' },
              { value: 'sanitation', label: 'Sanitation' },
              { value: 'other', label: 'Other' }
            ]}
            value={formData.category}
            onChange={(e) => setFormData({...formData, category: e.target.value})}
          />
          
          <div>
            <Input
              label="Location Address *"
              type="text"
              placeholder="Enter location"
              value={formData.address}
              onChange={(e) => setFormData({...formData, address: e.target.value})}
              required
            />
            <Button type="button" variant="ghost" size="sm" className="mt-2" onClick={handleUseLocation}>
              <MapPin size={16} />
              Use My Location {location && '✓'}
            </Button>
          </div>
          
          <FileUpload
            label="Attach Image (Optional)"
            accept="image/*"
            onChange={handleImageChange}
            preview={imagePreview && <img src={imagePreview} alt="Preview" className="rounded-lg max-h-48 object-cover" />}
            id="image-upload"
          />
          
          <FileUpload
            label="Attach Voice Note (Optional)"
            accept="audio/*"
            onChange={handleAudioChange}
            preview={audioFile && <audio controls className="w-full"><source src={URL.createObjectURL(audioFile)} /></audio>}
            id="audio-upload"
          />
          
          <Select
            label="Language"
            options={[
              { value: 'auto', label: 'Auto-detect' },
              { value: 'en', label: 'English' },
              { value: 'ta', label: 'Tamil' },
              { value: 'hi', label: 'Hindi' }
            ]}
            value={formData.language}
            onChange={(e) => setFormData({...formData, language: e.target.value})}
          />
          
          <div className="flex gap-4 pt-4">
            <Button type="submit" className="flex-1" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit Complaint'}
            </Button>
            <Button type="button" variant="outline" onClick={() => navigate('/')}>
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default SubmitComplaintPage;