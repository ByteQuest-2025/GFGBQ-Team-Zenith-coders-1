import logging
from typing import Dict
from ..ai.engine import get_ai_engine

logger = logging.getLogger(__name__)

class TriageClient:
    """
    AI Triage Client - now uses local AI engine instead of HTTP calls
    Provides same interface but with direct function calls for speed
    """
    
    async def triage_complaint(self, complaint: dict) -> dict:
        """
        Triage complaint using local AI engine
        
        Args:
            complaint: Complaint document with title and description
        
        Returns:
            dict: Triage results with category, confidence, urgency, etc.
        """
        try:
            # Get AI engine
            engine = get_ai_engine()
            
            # Prepare text
            text = f"{complaint['title']}. {complaint['description']}"
            language = complaint.get("language", "auto")
            
            # Process with AI
            logger.info(f" Triaging complaint with AI engine...")
            result = engine.process(text, language)
            
            logger.info(f" Triage complete: {result['category']} ({result['urgency_level']})")
            return result
        
        except Exception as e:
            logger.error(f" Triage failed: {e}")
            return self._fallback_triage(complaint)
    
    def _fallback_triage(self, complaint: dict) -> dict:
        """Fallback triage using simple keyword matching"""
        logger.info("🔄 Using fallback triage")
        
        text = f"{complaint['title']} {complaint['description']}".lower()
        
        category = "Administrative"
        urgency_level = "LOW"
        keywords = []
        
        if any(word in text for word in ["water", "electricity", "power", "light"]):
            category = "Utilities"
            keywords = ["utilities"]
            if any(word in text for word in ["no water", "power cut", "broken"]):
                urgency_level = "MEDIUM"
        elif any(word in text for word in ["garbage", "waste", "drain", "sewage"]):
            category = "Sanitation"
            keywords = ["sanitation"]
            urgency_level = "MEDIUM"
        elif any(word in text for word in ["safety", "crime", "theft", "danger"]):
            category = "Safety"
            keywords = ["safety"]
            urgency_level = "HIGH"
        elif any(word in text for word in ["health", "hospital", "doctor", "medical"]):
            category = "Health"
            keywords = ["health"]
            urgency_level = "MEDIUM"
        elif any(word in text for word in ["road", "pothole", "bridge", "traffic"]):
            category = "Infrastructure"
            keywords = ["infrastructure"]
            urgency_level = "MEDIUM"
        
        return {
            "category": category,
            "category_confidence": 0.5,
            "urgency_level": urgency_level,
            "urgency_score": 0.3 if urgency_level == "LOW" else (0.6 if urgency_level == "MEDIUM" else 0.9),
            "keywords_detected": keywords
        }

# Singleton instance
triage_client = TriageClient()
