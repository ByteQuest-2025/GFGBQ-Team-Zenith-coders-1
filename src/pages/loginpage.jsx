import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User } from 'lucide-react';
import { useAuth } from '../context/authcontext';
import { useToast } from '../context/toastcontext';
import Card from '../components/ui/card';
import Input from '../components/ui/input';
import Button from '../components/ui/button';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { showToast } = useToast();
  const [name, setName] = useState('');
  const [contact, setContact] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Mock login - replace with actual API call
      setTimeout(() => {
        login({ name, contact, token: 'demo-token-123' });
        showToast('Login successful!', 'success');
        navigate('/my');
        setLoading(false);
      }, 1000);
    } catch (error) {
      showToast('Login failed. Please try again.', 'error');
      setLoading(false);
    }
  };
  
  const handleDemoLogin = () => {
    login({ name: 'Demo Citizen', contact: 'demo@example.com', token: 'demo-token-123' });
    showToast('Logged in as Demo Citizen', 'success');
    navigate('/my');
  };
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-cyan-600 mx-auto mb-4 flex items-center justify-center">
            <User className="text-white" size={32} />
          </div>
          <h2 className="text-2xl font-bold">Welcome Back</h2>
          <p className="text-gray-600">Login to track your complaints</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Full Name"
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <Input
            label="Phone / Email"
            type="text"
            placeholder="Enter phone or email"
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            required
          />
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </Button>
        </form>
        
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">OR</span>
          </div>
        </div>
        
        <Button variant="outline" className="w-full" onClick={handleDemoLogin}>
          Continue as Demo Citizen
        </Button>
      </Card>
    </div>
  );
};

export default LoginPage;