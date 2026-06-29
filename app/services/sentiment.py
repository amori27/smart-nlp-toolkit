"""Sentiment classification using scikit-learn NaiveBayes + TF-IDF."""

from __future__ import annotations

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# ---------------------------------------------------------------------------
# Lightweight training data — enough for a demo / production microservice.
# In a real system you'd load from a file or S3.
# ---------------------------------------------------------------------------
_TRAINING_DATA = [
    ("I love this product, it works perfectly", "positive"),
    ("Absolutely amazing experience, highly recommend", "positive"),
    ("This is wonderful, I'm very happy with it", "positive"),
    ("Great quality and fast delivery", "positive"),
    ("Excellent service and friendly staff", "positive"),
    ("Best purchase I have ever made", "positive"),
    ("Outstanding performance, exceeds expectations", "positive"),
    ("Really impressed by the results", "positive"),
    ("Beautiful design and easy to use", "positive"),
    ("Fantastic value for the money", "positive"),
    ("This changed my life for the better", "positive"),
    ("Superb craftsmanship and attention to detail", "positive"),
    ("I am extremely satisfied with this", "positive"),
    ("Everything was perfect from start to finish", "positive"),
    ("What a delightful experience", "positive"),
    ("Thrilled with the outcome", "positive"),
    ("Incredible work, well done team", "positive"),
    ("This is exactly what I needed", "positive"),
    ("I appreciate the effort put into this", "positive"),
    ("The food was delicious and the atmosphere great", "positive"),
    ("This is terrible, I want a refund", "negative"),
    ("Worst experience of my life", "negative"),
    ("Very disappointing, do not recommend", "negative"),
    ("Poor quality, broke after one day", "negative"),
    ("Horrible customer service, rude staff", "negative"),
    ("Complete waste of money", "negative"),
    ("I hate this product so much", "negative"),
    ("Nothing works as advertised", "negative"),
    ("Disgusting food and dirty restaurant", "negative"),
    ("Awful experience, will never return", "negative"),
    ("This is the worst thing I have ever bought", "negative"),
    ("Frustrating and useless", "negative"),
    ("Extremely unhappy with the service", "negative"),
    ("Broken on arrival, cheap materials", "negative"),
    ("Terrible design, impossible to use", "negative"),
    ("Save your money and avoid this", "negative"),
    ("Pathetic excuse for a product", "negative"),
    ("I regret buying this immediately", "negative"),
    ("Shocking quality control", "negative"),
    ("Annoying bugs everywhere", "negative"),
    ("The weather is nice today", "neutral"),
    ("I went to the store this morning", "neutral"),
    ("The meeting is scheduled for Tuesday", "neutral"),
    ("She opened the door and walked inside", "neutral"),
    ("The book has three hundred pages", "neutral"),
    ("He drove to work this morning", "neutral"),
    ("The package arrived on time", "neutral"),
    ("I read the documentation", "neutral"),
    ("They discussed the project timeline", "neutral"),
    ("The file was uploaded successfully", "neutral"),
    ("We reviewed the quarterly report", "neutral"),
    ("The system is currently online", "neutral"),
    ("I received the email confirmation", "neutral"),
    ("The database backup completed", "neutral"),
    ("She updated the spreadsheet", "neutral"),
    ("The event starts at noon", "neutral"),
    ("We need to order more supplies", "neutral"),
    ("The train leaves at half past three", "neutral"),
]


def _build_model() -> Pipeline:
    """Train and return a TF-IDF + MultinomialNB pipeline."""
    texts, labels = zip(*_TRAINING_DATA)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_features=5000,
            lowercase=True,
        )),
        ("clf", MultinomialNB(alpha=0.1)),
    ])
    pipe.fit(texts, labels)
    return pipe


_model: Pipeline | None = None


def _get_model() -> Pipeline:
    global _model
    if _model is None:
        _model = _build_model()
    return _model


def classify_sentiment(text: str) -> dict:
    """Return sentiment label, confidence, and per-class scores."""
    model = _get_model()
    probs = model.predict_proba([text])[0]
    classes = list(model.classes_)
    scores = dict(zip(classes, probs.tolist()))
    best_idx = int(probs.argmax())
    label = classes[best_idx]
    confidence = round(float(probs[best_idx]), 4)
    scores_rounded = {k: round(v, 4) for k, v in scores.items()}
    return {
        "sentiment": label,
        "confidence": confidence,
        "scores": scores_rounded,
    }
