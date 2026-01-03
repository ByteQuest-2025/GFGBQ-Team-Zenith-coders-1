import httpx
import logging
from typing import Dict, Optional
from ..core.config import settings

logger = logging.getLogger(__name__)


class TriageClient:
    """
    Client for AI Triage Service (Coder 3's NLP service)
    Handles complaint classification and urgency detection
    
    Includes fallback logic if AI service is unavailable
    """
    
    def __init__(self):
        self.ai_service_url = settings.AI_SERVICE_URL
        self.timeout = 10.0  # 10 second timeout
    
    async def triage_complaint(self, complaint: dict) -> dict:
        """
        Send complaint to AI service for triage
        
        Args:
            complaint: Complaint document with title and description
        
        Returns:
            dict: Triage results with category, confidence, urgency, etc.
        """
        # Prepare payload for AI service
        payload = {
            "text": f"{complaint['title']}. {complaint['description']}",
            "language": complaint.get("language", "auto"),
            "location": complaint.get("location", {}).get("address", "")
        }
        
        try:
            logger.info(f"🤖 Sending complaint to AI triage service...")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.ai_service_url}/ai/triage",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"✅ Triage successful: {result.get('category', 'Unknown')} ({result.get('urgency_level', 'LOW')})")
                    return result
                else:
                    logger.warning(f"⚠️ AI service returned status {response.status_code}")
                    return self._fallback_triage(complaint)
        
        except httpx.TimeoutException:
            logger.error(f"❌ AI service timeout after {self.timeout}s")
            return self._fallback_triage(complaint)
        
        except httpx.ConnectError:
            logger.error(f"❌ Cannot connect to AI service at {self.ai_service_url}")
            return self._fallback_triage(complaint)
        
        except Exception as e:
            logger.error(f"❌ Triage service error: {e}")
            return self._fallback_triage(complaint)
    
    def _fallback_triage(self, complaint: dict) -> dict:
        """
        Fallback triage logic using simple keyword matching
        Used when AI service is unavailable
        
        Args:
            complaint: Complaint document
        
        Returns:
            dict: Basic triage result
        """
        logger.info("🔄 Using fallback triage (keyword-based)")
        
        text = f"{complaint['title']} {complaint['description']}".lower()
        
        # Simple keyword-based classification
        category = "Administrative"
        urgency_level = "LOW"
        keywords = []
        
        # Utilities
        if any(word in text for word in ["water", "electricity", "power", "light", "streetlight"]):
            category = "Utilities"
            keywords = ["utilities"]
            if any(word in text for word in ["no water", "power cut", "broken", "leak"]):
                urgency_level = "MEDIUM"
        
        # Sanitation
        elif any(word in text for word in ["garbage", "waste", "trash", "sanitation", "drain", "sewage"]):
            category = "Sanitation"
            keywords = ["sanitation"]
            if any(word in text for word in ["overflow", "smell", "block"]):
                urgency_level = "MEDIUM"
        
        # Safety
        elif any(word in text for word in ["safety", "crime", "theft", "police", "accident", "danger"]):
            category = "Safety"
            keywords = ["safety"]
            urgency_level = "HIGH"
        
        # Health
        elif any(word in text for word in ["health", "hospital", "doctor", "medical", "disease", "sick"]):
            category = "Health"
            keywords = ["health"]
            if any(word in text for word in ["emergency", "urgent", "critical"]):
                urgency_level = "HIGH"
            else:
                urgency_level = "MEDIUM"
        
        # Education
        elif any(word in text for word in ["school", "education", "teacher", "student"]):
            category = "Education"
            keywords = ["education"]
        
        return {
            "category": category,
            "category_confidence": 0.5,  # Low confidence for fallback
            "urgency_level": urgency_level,
            "urgency_score": 0.3 if urgency_level == "LOW" else (0.6 if urgency_level == "MEDIUM" else 0.9),
            "keywords_detected": keywords
        }


# Create singleton instance
triage_client = TriageClient()
