"""Tests for sentiment classification."""

import pytest
from app.services.sentiment import classify_sentiment


class TestSentiment:
    def test_positive(self):
        result = classify_sentiment("I love this product, it works perfectly")
        assert result["sentiment"] == "positive"
        assert result["confidence"] > 0.5

    def test_negative(self):
        result = classify_sentiment("This is terrible, I want a refund")
        assert result["sentiment"] == "negative"
        assert result["confidence"] > 0.5

    def test_neutral(self):
        result = classify_sentiment("The weather is nice today")
        assert result["sentiment"] == "neutral"
        assert "neutral" in result["scores"]

    def test_scores_sum_to_one(self):
        result = classify_sentiment("The meeting is scheduled for Tuesday")
        total = sum(result["scores"].values())
        assert abs(total - 1.0) < 0.01

    def test_confidence_between_zero_and_one(self):
        result = classify_sentiment("Absolutely amazing experience")
        assert 0.0 <= result["confidence"] <= 1.0

    def test_short_text(self):
        result = classify_sentiment("Great")
        assert result["sentiment"] in ("positive", "negative", "neutral")

    def test_long_text(self):
        text = "I love this " * 50
        result = classify_sentiment(text)
        assert result["sentiment"] in ("positive", "negative", "neutral")

    def test_unknown_words(self):
        result = classify_sentiment("xyzzy foobar qux")
        assert result["sentiment"] in ("positive", "negative", "neutral")
