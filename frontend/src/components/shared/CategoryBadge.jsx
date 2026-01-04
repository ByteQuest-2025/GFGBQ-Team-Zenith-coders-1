import { Badge } from '../ui/badge';

const categoryColors = {
  Infrastructure: 'bg-purple-100 text-purple-800',
  Sanitation: 'bg-green-100 text-green-800',
  Utilities: 'bg-blue-100 text-blue-800',
  Safety: 'bg-red-100 text-red-800',
  Health: 'bg-pink-100 text-pink-800',
  Administrative: 'bg-gray-100 text-gray-800',
};

export default function CategoryBadge({ category }) {
  if (!category) return null;
  
  return (
    <Badge variant="outline" className={`${categoryColors[category]} font-medium`}>
      {category}
    </Badge>
  );
}
