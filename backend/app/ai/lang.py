from langdetect import detect, LangDetectException
from googletrans import Translator
import logging

logger = logging.getLogger(__name__)
translator = Translator()

def detect_language(text: str) -> str:
    """Detect language of text"""
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def translate_to_english(text: str) -> tuple:
    """Translate text to English. Returns (translated_text, detected_language)"""
    try:
        detected = detect(text)
        if detected == 'en':
            return text, 'en'
        
        translation = translator.translate(text, src=detected, dest='en')
        return translation.text, detected
    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return text, "unknown"
