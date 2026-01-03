from app.ai.engine import AITriageEngine

# Initialize engine
print("🤖 Loading AI Engine...")
engine = AITriageEngine()
print("✅ AI Engine loaded\n")

# Test cases
test_cases = [
    {
        "text": "Garbage not collected for 5 days near school gate smells terrible",
        "expected_category": "Sanitation",
        "expected_urgency": "MEDIUM"
    },
    {
        "text": "Someone threatening me near bus stand need help urgently",
        "expected_category": "Safety",
        "expected_urgency": "HIGH"
    },
    {
        "text": "Road full of dangerous potholes causing accidents",
        "expected_category": "Infrastructure",
        "expected_urgency": "MEDIUM"
    },
    {
        "text": "No electricity since morning power cut affecting work",
        "expected_category": "Utilities",
        "expected_urgency": "MEDIUM"
    },
    {
        "text": "Hospital staff negligent patient suffering emergency",
        "expected_category": "Health",
        "expected_urgency": "HIGH"
    },
    {
        "text": "Birth certificate application pending for 3 months",
        "expected_category": "Administrative",
        "expected_urgency": "LOW"
    }
]

# Run tests
print("🧪 Testing AI Engine with sample complaints:\n")
correct = 0
total = len(test_cases)

for i, test in enumerate(test_cases, 1):
    print(f"Test {i}/{total}")
    print(f"Input: {test['text']}")
    
    result = engine.process(test['text'], language="auto")
    
    print(f"✅ Category: {result['category']} (confidence: {result['category_confidence']:.2f})")
    print(f"✅ Urgency: {result['urgency_level']} (score: {result['urgency_score']:.2f})")
    print(f"✅ Keywords: {', '.join(result['keywords_detected'][:5])}")
    
    # Check if correct
    category_match = result['category'] == test['expected_category']
    urgency_match = result['urgency_level'] == test['expected_urgency']
    
    if category_match and urgency_match:
        correct += 1
        print("✅ PASS\n")
    else:
        print(f"⚠️  Expected: {test['expected_category']} / {test['expected_urgency']}\n")

print(f"📊 Test Results: {correct}/{total} passed ({correct/total*100:.1f}%)")
