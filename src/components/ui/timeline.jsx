import React from 'react';
import { CheckCircle } from 'lucide-react';
import { formatDateTime } from '../../lib/utils';

const Timeline = ({ items }) => (
  <div className="space-y-4">
    {items.map((item, idx) => (
      <div key={idx} className="flex gap-4">
        <div className="flex flex-col items-center">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${idx === items.length - 1 ? 'bg-gradient-to-r from-blue-600 to-cyan-600' : 'bg-gray-200'}`}>
            <CheckCircle className="text-white" size={20} />
          </div>
          {idx < items.length - 1 && <div className="w-0.5 h-full bg-gray-200 my-1"></div>}
        </div>
        <div className="flex-1 pb-8">
          <div className="font-semibold text-gray-900">{item.status.replace('_', ' ')}</div>
          <div className="text-sm text-gray-600">{formatDateTime(item.timestamp)}</div>
          {item.notes && <div className="text-sm text-gray-500 mt-1">{item.notes}</div>}
        </div>
      </div>
    ))}
  </div>
);

export default Timeline;