import React, { useEffect } from 'react';
import { CheckCircle, AlertCircle, Bell, X } from 'lucide-react';

const Toast = ({ message, type = 'success', onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000);
    return () => clearTimeout(timer);
  }, [onClose]);
  
  const icons = {
    success: <CheckCircle className="text-green-500" />,
    error: <AlertCircle className="text-red-500" />,
    info: <Bell className="text-blue-500" />
  };
  
  return (
    <div className="bg-white rounded-lg shadow-xl p-4 flex items-center gap-3 animate-slide-in min-w-[300px]">
      {icons[type]}
      <p className="flex-1 font-medium">{message}</p>
      <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
        <X size={18} />
      </button>
    </div>
  );
};

export default Toast;