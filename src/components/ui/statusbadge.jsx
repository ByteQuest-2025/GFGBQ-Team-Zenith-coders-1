import React from 'react';
import { Clock, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import Badge from './badge';

const StatusBadge = ({ status }) => {
  const config = {
    SUBMITTED: { variant: 'info', icon: Clock, label: 'SUBMITTED' },
    TRIAGED: { variant: 'info', icon: CheckCircle, label: 'TRIAGED' },
    ASSIGNED: { variant: 'warning', icon: AlertCircle, label: 'ASSIGNED' },
    IN_PROGRESS: { variant: 'warning', icon: RefreshCw, label: 'IN PROGRESS' },
    RESOLVED: { variant: 'success', icon: CheckCircle, label: 'RESOLVED' }
  };
  
  const { variant, icon: Icon, label } = config[status] || config.SUBMITTED;
  
  return (
    <Badge variant={variant} className="gap-1">
      <Icon size={12} />
      {label}
    </Badge>
  );
};

export default StatusBadge;