import React from 'react';

const Card = ({ children, className = '', hover = false, onClick }) => (
  <div 
    className={`bg-white rounded-xl shadow-md p-6 ${hover ? 'hover:shadow-xl transition-shadow cursor-pointer' : ''} ${className}`}
    onClick={onClick}
  >
    {children}
  </div>
);

export default Card;