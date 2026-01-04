import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { complaintAPI } from '../../services/api';
import toast from 'react-hot-toast';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Textarea } from '../ui/textarea';
import { Label } from '../ui/label';
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from '../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { MapPin, Upload, Loader2, Keyboard, Mic } from 'lucide-react';
import VoiceInput from './VoiceInput';

const complaintSchema = z.object({
  title: z.string().min(5, 'Title must be at least 5 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  address: z.string().min(5, 'Address is required'),
  latitude: z.string().optional(),
  longitude: z.string().optional(),
});

export default function ComplaintForm({ onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [image, setImage] = useState(null);
  const [locationLoading, setLocationLoading] = useState(false);
  const [inputMode, setInputMode] = useState('text');
  
  const { register, handleSubmit, formState: { errors }, setValue, watch, reset } = useForm({
    resolver: zodResolver(complaintSchema),
  });
  
  const getCurrentLocation = () => {
    setLocationLoading(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setValue('latitude', position.coords.latitude.toString());
          setValue('longitude', position.coords.longitude.toString());
          toast.success('Location captured successfully');
          setLocationLoading(false);
        },
        () => {
          toast.error('Unable to get location');
          setLocationLoading(false);
        }
      );
    } else {
      toast.error('Geolocation not supported');
      setLocationLoading(false);
    }
  };
  
  const handleVoiceTranscript = (transcript) => {
    // Auto-fill description from voice input
    const currentDesc = watch('description') || '';
    setValue('description', currentDesc + ' ' + transcript);
  };
  
  const onSubmit = async (data) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('title', data.title);
      formData.append('description', data.description);
      formData.append('address', data.address);
      formData.append('language', 'auto');
      
      if (data.latitude) formData.append('latitude', parseFloat(data.latitude));
      if (data.longitude) formData.append('longitude', parseFloat(data.longitude));
      if (image) formData.append('image', image);
      
      const response = await complaintAPI.create(formData);
      toast.success('Complaint submitted successfully! AI is analyzing...');
      reset();
      setImage(null);
      onSuccess?.(response.data);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to submit complaint');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>Submit New Complaint</CardTitle>
        <CardDescription>
          Your complaint will be automatically classified and routed using AI
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={inputMode} onValueChange={setInputMode} className="mb-4">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="text">
              <Keyboard className="w-4 h-4 mr-2" />
              Text Input
            </TabsTrigger>
            <TabsTrigger value="voice">
              <Mic className="w-4 h-4 mr-2" />
              Voice Input
            </TabsTrigger>
          </TabsList>
        </Tabs>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {inputMode === 'voice' && (
            <VoiceInput 
              onTranscript={handleVoiceTranscript}
            />
          )}

          <div>
            <Label htmlFor="title">Complaint Title *</Label>
            <Input 
              id="title"
              {...register('title')} 
              placeholder="Brief description of the issue"
              className="mt-1"
            />
            {errors.title && (
              <p className="text-red-500 text-sm mt-1">{errors.title.message}</p>
            )}
          </div>
          
          <div>
            <Label htmlFor="description">Detailed Description *</Label>
            <Textarea 
              id="description"
              {...register('description')} 
              rows={6} 
              placeholder="Provide detailed information about the issue"
              className="mt-1"
            />
            {errors.description && (
              <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
            )}
            <p className="text-xs text-gray-500 mt-1">
              Use voice input above or type directly. Voice transcript will appear here.
            </p>
          </div>
          
          <div>
            <Label htmlFor="address">Location Address *</Label>
            <Input 
              id="address"
              {...register('address')} 
              placeholder="Street, Area, City"
              className="mt-1"
            />
            {errors.address && (
              <p className="text-red-500 text-sm mt-1">{errors.address.message}</p>
            )}
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="latitude">Latitude</Label>
              <Input 
                id="latitude"
                {...register('latitude')}
                placeholder="Auto-captured"
                type="number"
                step="any"
                className="mt-1"
                readOnly
              />
            </div>
            <div>
              <Label htmlFor="longitude">Longitude</Label>
              <Input 
                id="longitude"
                {...register('longitude')}
                placeholder="Auto-captured"
                type="number"
                step="any"
                className="mt-1"
                readOnly
              />
            </div>
          </div>
          
          <Button 
            type="button" 
            variant="outline" 
            onClick={getCurrentLocation}
            disabled={locationLoading}
            className="w-full"
          >
            {locationLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Getting Location...
              </>
            ) : (
              <>
                <MapPin className="mr-2 h-4 w-4" />
                Capture Current Location
              </>
            )}
          </Button>
          
          <div>
            <Label htmlFor="image">Upload Image (Optional)</Label>
            <div className="mt-1 flex items-center gap-2">
              <Input 
                id="image"
                type="file" 
                accept="image/*" 
                onChange={(e) => setImage(e.target.files[0])}
              />
              {image && (
                <span className="text-sm text-green-600">Selected</span>
              )}
            </div>
          </div>
          
          <Button type="submit" className="w-full" disabled={loading} size="lg">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              'Submit Complaint'
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
