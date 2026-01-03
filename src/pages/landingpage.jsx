import React from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertCircle, Clock, CheckCircle, ChevronRight } from 'lucide-react';
import Button from '../components/ui/button';
import Card from '../components/ui/card';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-cyan-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">AI-Powered Grievance Redressal</h1>
          <p className="text-xl mb-8 text-blue-100">Smart complaint management for faster, transparent public service delivery</p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button variant="secondary" size="lg" onClick={() => navigate('/submit')}>
              Submit a Complaint
              <ChevronRight size={20} />
            </Button>
            <Button variant="outline" size="lg" className="bg-white/10 border-white text-white hover:bg-white/20" onClick={() => navigate('/my')}>
              Track Complaints
            </Button>
          </div>
        </div>
      </div>
      
      {/* Features */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <Card className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-cyan-600 mx-auto mb-4 flex items-center justify-center">
              <AlertCircle className="text-white" size={32} />
            </div>
            <h3 className="font-bold text-xl mb-2">AI Categorization</h3>
            <p className="text-gray-600">Advanced AI automatically categorizes complaints into relevant departments with 95%+ accuracy</p>
          </Card>
          
          <Card className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-green-600 to-emerald-600 mx-auto mb-4 flex items-center justify-center">
              <Clock className="text-white" size={32} />
            </div>
            <h3 className="font-bold text-xl mb-2">Urgency Prioritization</h3>
            <p className="text-gray-600">Smart urgency detection ensures critical issues are addressed first, reducing response time by 60%</p>
          </Card>
          
          <Card className="text-center">
            <div className="w-16 h-16 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 mx-auto mb-4 flex items-center justify-center">
              <CheckCircle className="text-white" size={32} />
            </div>
            <h3 className="font-bold text-xl mb-2">Transparent Tracking</h3>
            <p className="text-gray-600">Real-time status updates with complete timeline visibility for accountability and trust</p>
          </Card>
        </div>
      </div>
      
      {/* Impact Stats */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">95%</div>
              <div className="text-gray-600">AI Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">60%</div>
              <div className="text-gray-600">Faster Resolution</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">24/7</div>
              <div className="text-gray-600">Available</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">100%</div>
              <div className="text-gray-600">Transparent</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;