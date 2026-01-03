import joblib
import logging
from typing import Dict, Any
from .preprocess import preprocess_text
from .keywords import detect_urgency_keywords, match_keywords, CATEGORY_KEYWORDS
from .lang import detect_language, translate_to_english

logger = logging.getLogger(__name__)

class AITriageEngine:
    """Main AI Triage Engine for complaint classification"""
    
    def __init__(self, model_path="app/ai/models"):
        try:
            self.vectorizer = joblib.load(f"{model_path}/tfidf_vectorizer.joblib")
            self.model = joblib.load(f"{model_path}/category_model.joblib")
            self.label_encoder = joblib.load(f"{model_path}/label_encoder.joblib")
            logger.info("AI Triage Engine initialized")
        except Exception as e:
            logger.error(f"Failed to load AI models: {e}")
            raise
    
    def process(self, text: str, language: str = "auto") -> Dict[str, Any]:
        """Main processing pipeline"""
        detected_lang = detect_language(text)
        if language == "auto" and detected_lang != "en":
            try:
                translated_text, detected_lang = translate_to_english(text)
            except:
                translated_text = text
                detected_lang = "en"
        else:
            translated_text = text
        
        normalized_text = preprocess_text(translated_text)
        
        category, confidence = self._classify_category(normalized_text)
        
        # Only use keyword fallback if ML confidence is very low
        if confidence < 0.35:
            category_scores, matched_keywords_dict = match_keywords(normalized_text, CATEGORY_KEYWORDS)
            if category_scores:
                keyword_category = max(category_scores, key=category_scores.get)
                if category_scores[keyword_category] >= 2:
                    category = keyword_category
                    confidence = min(0.50 + (category_scores[keyword_category] * 0.05), 0.75)

        
        urgency_level, urgency_score, urgency_keywords = self._detect_urgency(normalized_text, category)
        
        category_scores, matched_keywords_dict = match_keywords(normalized_text, CATEGORY_KEYWORDS)
        all_keywords = urgency_keywords + matched_keywords_dict.get(category, [])
        
        return {
            "category": category,
            "category_confidence": round(float(confidence), 4),
            "urgency_level": urgency_level,
            "urgency_score": round(float(urgency_score), 4),
            "keywords_detected": list(set(all_keywords[:15])),
            "language_detected": detected_lang,
            "normalized_text": normalized_text,
            "model_version": "tfidf_lr_v1"
        }
    
    def _classify_category(self, text: str) -> tuple:
        """Classify complaint category"""
        try:
            X = self.vectorizer.transform([text])
            pred_idx = self.model.predict(X)[0]
            pred_proba = self.model.predict_proba(X)[0]
            
            confidence = pred_proba[pred_idx]
            category = self.label_encoder.classes_[pred_idx]
            
            return category, confidence
        except Exception as e:
            logger.error(f"Classification error: {e}")
            return "Administrative", 0.0
    
    def _detect_urgency(self, text: str, category: str) -> tuple:
        """Detect urgency level"""
        urgency_level, urgency_score, keywords = detect_urgency_keywords(text)
        
        # Apply category boosts only to base score
        boosted_score = urgency_score
        
        if category == "Safety":
            boosted_score = min(urgency_score + 0.20, 1.0)
        elif category == "Health":
            boosted_score = min(urgency_score + 0.15, 1.0)
        elif category in ["Sanitation", "Utilities", "Infrastructure"]:
            boosted_score = min(urgency_score + 0.10, 1.0)
        
        # Determine final level with stricter thresholds
        if boosted_score >= 0.70:
            final_level = "HIGH"
        elif boosted_score >= 0.30:
            final_level = "MEDIUM"
        else:
            final_level = "LOW"
        
        return final_level, boosted_score, keywords



ai_engine = None

def get_ai_engine():
    """Get the global AI engine instance"""
    global ai_engine
    if ai_engine is None:
        raise RuntimeError("AI Engine not initialized")
    return ai_engine

def initialize_ai_engine():
    """Initialize the AI engine at startup"""
    global ai_engine
    ai_engine = AITriageEngine()
    return ai_engine
