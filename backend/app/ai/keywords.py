"""Keyword dictionaries for category matching and urgency detection"""

CATEGORY_KEYWORDS = {
    "Infrastructure": [
        "road", "pothole", "potholes", "bridge", "traffic", "signal", "footpath", "street", 
        "pavement", "highway", "divider", "barrier", "manhole", "cover", "crossing", "zebra", 
        "lane", "sidewalk", "pathway", "guardrail", "footbridge", "stairs", "bench", "shelter",
        "sign", "board", "marking", "speed", "breaker", "flyover", "subway"
    ],
    "Sanitation": [
        "garbage", "waste", "trash", "dustbin", "sewage", "drain", "drainage", "toilet",
        "sanitation", "dirty", "smell", "smells", "smelly", "stink", "overflow", "dump", "dumping",
        "litter", "compost", "septic", "gutter", "clogged", "blocked", "plastic",
        "pollution", "hygiene", "unhygienic", "cleaning", "sweeper", "bins", "collected"
    ],
    "Utilities": [
        "water", "electricity", "power", "current", "supply", "outage", "cut", "broadband",
        "internet", "wifi", "cable", "connection", "meter", "transformer", "pole", "wire",
        "pipeline", "tanker", "motor", "pump", "voltage", "fluctuation", "fiber", "network",
        "billing", "bill", "pressure", "leakage", "contaminated", "streetlight", "light"
    ],
    "Safety": [
        "unsafe", "danger", "dangerous", "threat", "threatening", "harassment", "assault", 
        "attack", "robbery", "theft", "stealing", "violence", "fight", "fighting", "crime", 
        "criminal", "stalking", "molest", "rape", "murder", "kidnap", "extortion", "arson", 
        "fire", "accident", "accidents", "injury", "hurt", "bleeding", "weapon", "gun", "knife", 
        "scared", "fear", "police", "security", "patrol"
    ],
    "Health": [
        "hospital", "doctor", "medicine", "medical", "health", "disease", "illness", "sick",
        "patient", "treatment", "clinic", "vaccine", "vaccination", "epidemic", "outbreak",
        "fever", "dengue", "malaria", "tuberculosis", "covid", "infection", "virus", "bacteria",
        "ambulance", "emergency", "blood", "oxygen", "bed", "icu", "surgery", "negligent",
        "contaminated", "poisoning", "mental", "suffering"
    ],
    "Administrative": [
        "certificate", "document", "application", "pending", "delay", "delayed", "approval", 
        "license", "permit", "registration", "verification", "aadhaar", "passport", "voter", 
        "ration", "card", "pension", "tax", "office", "staff", "officer", "corruption", "bribe",
        "rti", "grievance", "complaint", "service", "portal", "online", "submission", "refund",
        "processing", "rejection", "mutation", "property", "land", "record"
    ]
}

URGENCY_KEYWORDS = {
    "HIGH": [
        "death", "die", "dying", "dead", "kill", "murder", "suicide",
        "injured", "bleeding", "unconscious", "critical",
        "fire", "explosion", "bomb", "weapon", "gun", "knife",
        "rape", "kidnap", "assault", "attack", "robbery", "violence",
        "urgent", "urgently", "immediately", "asap", "emergency",
        "threat", "threatening", "help"
    ],
    "MEDIUM": [
        "unsafe", "risk", "hazard", "broken", "damaged", "not working",
        "malfunction", "overflow", "blocked", "smell", "smells",
        "negligent", "suffering", "problem", "terrible"
    ]
}

def detect_urgency_keywords(text: str) -> tuple:
    """Detect urgency level based on keywords"""
    text_lower = text.lower()
    
    high_keywords = [kw for kw in URGENCY_KEYWORDS["HIGH"] if kw in text_lower]
    medium_keywords = [kw for kw in URGENCY_KEYWORDS["MEDIUM"] if kw in text_lower]
    
    # Base scoring - reduced weights
    high_score = len(high_keywords) * 0.35
    medium_score = len(medium_keywords) * 0.12
    urgency_score = min(high_score + medium_score, 1.0)
    
    # Determine initial level without category boost
    if high_score >= 0.35:
        urgency_level = "HIGH"
    elif medium_score >= 0.24 or (high_score > 0 and medium_score > 0):
        urgency_level = "MEDIUM"
    else:
        urgency_level = "LOW"
    
    all_keywords = high_keywords + medium_keywords
    return urgency_level, urgency_score, list(set(all_keywords[:10]))

def match_keywords(text: str, keyword_dict: dict) -> dict:
    """Match keywords from text and return category scores"""
    text_lower = text.lower()
    scores = {}
    matched_keywords = {}
    
    for category, keywords in keyword_dict.items():
        matches = [kw for kw in keywords if kw in text_lower]
        scores[category] = len(matches)
        if matches:
            matched_keywords[category] = matches
    
    return scores, matched_keywords
