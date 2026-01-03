import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
from .preprocess import preprocess_text

def train_model():
    """Train the AI triage model"""
    print("Loading training data...")
    
    if not os.path.exists("data/complaints_train.csv"):
        print("ERROR: Training data not found. Run data/generate_dataset.py first")
        return
    
    train_df = pd.read_csv("data/complaints_train.csv")
    test_df = pd.read_csv("data/complaints_test.csv")
    
    print(f"Loaded {len(train_df)} training samples, {len(test_df)} test samples")
    print(f"Categories: {train_df['category'].unique()}")
    
    # Preprocess
    print("\nPreprocessing text...")
    train_df['processed'] = train_df['text'].apply(preprocess_text)
    test_df['processed'] = test_df['text'].apply(preprocess_text)
    
    # Remove any empty processed texts
    train_df = train_df[train_df['processed'].str.len() > 0]
    test_df = test_df[test_df['processed'].str.len() > 0]
    
    print(f"After preprocessing: {len(train_df)} training, {len(test_df)} test samples")
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_df['category'])
    y_test = label_encoder.transform(test_df['category'])
    
    print(f"\nLabel encoding complete:")
    for idx, label in enumerate(label_encoder.classes_):
        print(f"  {idx}: {label}")
    
    # Vectorize with improved parameters
    print("\nCreating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=3000,
        min_df=1,
        max_df=0.9,
        sublinear_tf=True,
        strip_accents='unicode'
    )
    
    X_train = vectorizer.fit_transform(train_df['processed'])
    X_test = vectorizer.transform(test_df['processed'])
    
    print(f"Feature matrix shape: {X_train.shape}")
    
    # Train model with sklearn-compatible parameters
    print("\nTraining Logistic Regression model...")
    model = LogisticRegression(
        max_iter=3000,
        C=2.0,
        class_weight='balanced',
        random_state=42,
        solver='lbfgs'
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate on training set
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    print(f"\nTraining Accuracy: {train_accuracy:.3f}")
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {test_accuracy:.3f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Show prediction confidence
    print("\nPrediction Confidence Statistics:")
    max_proba = y_pred_proba.max(axis=1)
    print(f"  Mean confidence: {max_proba.mean():.3f}")
    print(f"  Min confidence: {max_proba.min():.3f}")
    print(f"  Max confidence: {max_proba.max():.3f}")
    
    # Save models
    os.makedirs("app/ai/models", exist_ok=True)
    joblib.dump(vectorizer, "app/ai/models/tfidf_vectorizer.joblib")
    joblib.dump(model, "app/ai/models/category_model.joblib")
    joblib.dump(label_encoder, "app/ai/models/label_encoder.joblib")
    
    print("\nModels saved successfully to app/ai/models/")
    print("Training complete!")
    
    return test_accuracy

if __name__ == "__main__":
    train_model()
