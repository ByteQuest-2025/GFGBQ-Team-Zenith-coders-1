from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)

class DuplicateDetector:
    """Service for detecting duplicate/similar complaints"""
    
    def __init__(self):
        self.similarity_threshold = 0.75  # 75% similarity to be considered duplicate
        self.time_window_days = 30  # Only check complaints from last 30 days
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for comparison"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity score between two texts"""
        clean1 = self.clean_text(text1)
        clean2 = self.clean_text(text2)
        
        if not clean1 or not clean2:
            return 0.0
        
        # Use SequenceMatcher for basic similarity
        return SequenceMatcher(None, clean1, clean2).ratio()
    
    def extract_keywords(self, text: str) -> set:
        """Extract important keywords from text"""
        clean = self.clean_text(text)
        words = clean.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this', 'that',
            'from', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had'
        }
        
        keywords = {word for word in words if len(word) > 3 and word not in stop_words}
        return keywords
    
    def keyword_overlap(self, text1: str, text2: str) -> float:
        """Calculate keyword overlap between two texts"""
        keywords1 = self.extract_keywords(text1)
        keywords2 = self.extract_keywords(text2)
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def location_similarity(self, loc1: Dict, loc2: Dict) -> bool:
        """Check if two locations are similar"""
        if not loc1 or not loc2:
            return False
        
        # Check if addresses are similar
        addr1 = loc1.get('address', '')
        addr2 = loc2.get('address', '')
        
        if addr1 and addr2:
            similarity = self.calculate_similarity(addr1, addr2)
            if similarity > 0.6:
                return True
        
        # Check if coordinates are close (within ~500m)
        lat1 = loc1.get('latitude')
        lon1 = loc1.get('longitude')
        lat2 = loc2.get('latitude')
        lon2 = loc2.get('longitude')
        
        if all([lat1, lon1, lat2, lon2]):
            # Simple distance check (rough approximation)
            lat_diff = abs(lat1 - lat2)
            lon_diff = abs(lon1 - lon2)
            
            # ~0.005 degrees is approximately 500m
            if lat_diff < 0.005 and lon_diff < 0.005:
                return True
        
        return False
    
    def find_duplicates(
        self,
        new_complaint: Dict,
        existing_complaints: List[Dict],
        check_location: bool = True
    ) -> List[Dict]:
        """
        Find potential duplicate complaints
        
        Returns list of similar complaints with similarity scores
        """
        duplicates = []
        
        new_title = new_complaint.get('title', '')
        new_desc = new_complaint.get('description', '')
        new_category = new_complaint.get('category', '')
        new_location = new_complaint.get('location', {})
        
        # Combined text for comparison
        new_text = f"{new_title} {new_desc}"
        
        for existing in existing_complaints:
            # Skip if different category
            if existing.get('category') != new_category:
                continue
            
            # Skip if too old
            created_at = existing.get('created_at')
            if created_at:
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                if datetime.utcnow() - created_at > timedelta(days=self.time_window_days):
                    continue
            
            # Calculate text similarity
            existing_title = existing.get('title', '')
            existing_desc = existing.get('description', '')
            existing_text = f"{existing_title} {existing_desc}"
            
            text_similarity = self.calculate_similarity(new_text, existing_text)
            keyword_similarity = self.keyword_overlap(new_text, existing_text)
            
            # Average of both similarities
            overall_similarity = (text_similarity + keyword_similarity) / 2
            
            # Check location if required
            location_match = True
            if check_location:
                existing_location = existing.get('location', {})
                location_match = self.location_similarity(new_location, existing_location)
            
            # Consider it a duplicate if similarity is high
            if overall_similarity >= self.similarity_threshold and location_match:
                duplicates.append({
                    'complaint_id': existing.get('complaint_id'),
                    'title': existing_title,
                    'similarity_score': round(overall_similarity, 2),
                    'status': existing.get('status'),
                    'created_at': existing.get('created_at')
                })
        
        # Sort by similarity score (highest first)
        duplicates.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return duplicates
    
    def check_for_duplicates(
        self,
        complaint: Dict,
        db_complaints: List[Dict]
    ) -> Optional[Dict]:
        """
        Check if a complaint is a duplicate
        
        Returns:
            Dict with duplicate info if found, None otherwise
        """
        duplicates = self.find_duplicates(complaint, db_complaints)
        
        if duplicates:
            logger.info(f"Found {len(duplicates)} potential duplicates")
            return {
                'is_duplicate': True,
                'duplicate_count': len(duplicates),
                'similar_complaints': duplicates[:5],  # Return top 5
                'primary_duplicate': duplicates[0] if duplicates else None
            }
        
        return {
            'is_duplicate': False,
            'duplicate_count': 0,
            'similar_complaints': []
        }

duplicate_detector = DuplicateDetector()
