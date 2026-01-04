import { Badge } from '../ui/badge';

const statusColors = {
  SUBMITTED: 'bg-gray-500',
  TRIAGED: 'bg-blue-500',
  ASSIGNED: 'bg-yellow-500',
  IN_PROGRESS: 'bg-orange-500',
  RESOLVED: 'bg-green-500',
  REJECTED: 'bg-red-500',
};

export default function StatusBadge({ status }) {
  return (
    <Badge className={`${statusColors[status]} text-white`}>
      {status?.replace('_', ' ')}
    </Badge>
  );
}
