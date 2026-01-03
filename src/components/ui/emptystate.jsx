import React from 'react';
import { AlertCircle } from 'lucide-react';

const EmptyState = ({ title, description, action }) => (
  <div className="text-center py-12">
    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
      <AlertCircle className="text-gray-400" size={32} />
    </div>
    <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
    <p className="text-gray-600 mb-6">{description}</p>
    {action}
  </div>
);

export default EmptyState;