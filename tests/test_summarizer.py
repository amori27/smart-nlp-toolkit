"""Tests for extractive summarization."""

import pytest
from app.services.summarizer import summarize_text


class TestSummarizer:
    def test_short_text(self):
        result = summarize_text("This is a short sentence.")
        assert "short" in result["summary"].lower()

    def test_longer_text(self):
        text = (
            "Artificial intelligence has transformed many industries. "
            "Healthcare providers use AI for diagnostics and treatment planning. "
            "Financial institutions rely on machine learning for fraud detection. "
            "Manufacturing plants deploy robots powered by AI for quality control. "
            "Retail companies use recommendation systems to personalize shopping. "
            "Transportation networks optimize routes using predictive algorithms. "
            "Education platforms adapt content to individual learner needs. "
            "Agriculture benefits from AI-driven crop monitoring systems."
        )
        result = summarize_text(text, num_sentences=3)
        assert result["num_sentences_summary"] == 3
        assert result["num_sentences_original"] == 8
        assert result["summary_length"] < result["original_length"]
        assert result["compression_ratio"] < 1.0

    def test_compression_ratio(self):
        result = summarize_text("One. Two. Three. Four. Five.")
        assert 0.0 <= result["compression_ratio"] <= 1.0

    def test_num_sentences_larger_than_text(self):
        result = summarize_text("Just one sentence here.", num_sentences=5)
        assert result["num_sentences_summary"] == 1

    def test_summary_in_original(self):
        text = "The capital of France is Paris. The capital of Japan is Tokyo."
        result = summarize_text(text)
        assert result["summary_length"] <= result["original_length"]
