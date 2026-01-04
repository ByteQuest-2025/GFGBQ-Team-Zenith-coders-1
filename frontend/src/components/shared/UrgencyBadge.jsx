import { Badge } from '../ui/badge';

const urgencyConfig = {
  HIGH: { color: 'bg-red-100 text-red-800 border-red-300', icon: '🔴' },
  MEDIUM: { color: 'bg-yellow-100 text-yellow-800 border-yellow-300', icon: '🟡' },
  LOW: { color: 'bg-green-100 text-green-800 border-green-300', icon: '🟢' },
};

export default function UrgencyBadge({ level }) {
  if (!level) return null;
  const config = urgencyConfig[level] || urgencyConfig.LOW;
  
  return (
    <Badge variant="outline" className={`${config.color} font-medium`}>
      {config.icon} {level}
    </Badge>
  );
}
