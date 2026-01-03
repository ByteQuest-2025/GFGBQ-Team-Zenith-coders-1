import re

def preprocess_text(text: str) -> str:
    """Clean and normalize complaint text"""
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'\S+@\S+', '', text)  # Remove emails
    text = re.sub(r'(\+91|0)?[6-9]\d{9}', '', text)  # Remove phone numbers
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove emojis
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)  # Keep alphanumeric
    text = text.strip()
    
    return text
