// src/components/ui/UrgencyBadge.jsx
import React from 'react';
import Badge from './badge'; // Make sure this file exists as Badge.jsx or Badge.js with default export

/**
 * UrgencyBadge component
 * @param {string} level - "HIGH", "MEDIUM", "LOW"
 * @param {number} score - optional score 0-1
 */
const UrgencyBadge = ({ level, score }) => {
  // Configuration for different levels
  const config = {
    HIGH: { variant: 'danger', label: 'High Priority' },
    MEDIUM: { variant: 'warning', label: 'Medium Priority' },
    LOW: { variant: 'default', label: 'Low Priority' },
  };

  const { variant, label } = config[level] || config.MEDIUM;

  return (
    <Badge variant={variant}>
      {label} {score !== undefined && `(${Math.round(score * 100)}%)`}
    </Badge>
  );
};

export default UrgencyBadge;
