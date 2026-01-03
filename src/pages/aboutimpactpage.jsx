import React from 'react';
import { CheckCircle, AlertCircle, Bell, User } from 'lucide-react';
import Card from '../components/ui/card'; // ✅ ensure correct case

const AboutImpactPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold mb-4">About GrievanceAI</h1>
        <p className="text-xl text-gray-600">
          Transforming public governance through AI-powered complaint management
        </p>
      </div>

      <Card className="mb-8">
        <h2 className="text-2xl font-bold mb-6">Social Impact</h2>

        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center justify-center flex-shrink-0">
              <CheckCircle className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Faster Resolution Times</h3>
              <p className="text-gray-600">
                AI-powered triage and routing reduces average resolution time by 60%, ensuring citizens get help when they need it most.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-green-600 to-emerald-600 flex items-center justify-center flex-shrink-0">
              <AlertCircle className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Improved Accountability</h3>
              <p className="text-gray-600">
                Complete transparency in complaint tracking builds trust between citizens and government, with every step documented.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center flex-shrink-0">
              <User className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Inclusive Access</h3>
              <p className="text-gray-600">
                Multi-language support and voice input ensure everyone can file complaints, regardless of literacy or technical skills.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-r from-orange-500 to-red-500 flex items-center justify-center flex-shrink-0">
              <Bell className="text-white" size={24} />
            </div>
            <div>
              <h3 className="font-semibold text-lg">Data-Driven Insights</h3>
              <p className="text-gray-600">
                Aggregated complaint patterns help identify systemic issues and inform policy decisions for better governance.
              </p>
            </div>
          </div>
        </div>
      </Card>

      <Card>
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>

        <div className="space-y-6">
          {[
            ['Citizen Submits Complaint', 'Through web or mobile, with text, voice, or images in any language'],
            ['AI Processes & Classifies', 'Natural language processing categorizes complaint and assesses urgency automatically'],
            ['Smart Routing', 'System routes to appropriate department and officer based on category and location'],
            ['Real-time Tracking', 'Citizen receives updates at every stage until resolution, with full timeline visibility']
          ].map((step, index) => (
            <div key={index} className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center justify-center text-white font-bold flex-shrink-0">
                {index + 1}
              </div>
              <div>
                <h3 className="font-semibold text-lg mb-1">{step[0]}</h3>
                <p className="text-gray-600">{step[1]}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default AboutImpactPage;
