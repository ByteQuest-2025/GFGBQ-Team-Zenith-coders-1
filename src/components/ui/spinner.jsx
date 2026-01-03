import React from 'react';

const Spinner = ({ size = 'md' }) => {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16'
  };

  return (
    <div className="flex justify-center items-center p-8">
      <div className={`animate-spin rounded-full border-4 border-blue-500 border-t-transparent ${sizes[size]}`}></div>
    </div>
  );
};

export default Spinner;