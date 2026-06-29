"""Tests for readability analysis."""

import pytest
from app.services.readability import analyze_readability, _count_syllables


class TestReadability:
    def test_simple_text(self):
        result = analyze_readability("The cat sat on the mat.")
        assert result["flesch_kincaid_grade"] >= 0
        assert result["flesch_reading_ease"] > 0
        assert result["total_words"] == 6
        assert result["total_sentences"] == 1

    def test_complex_text(self):
        text = "The multidisciplinary investigation demonstrated significant correlation between variables"
        result = analyze_readability(text)
        assert result["flesch_kincaid_grade"] > 0
        assert result["level"] in (
            "Elementary", "Middle School", "High School", "College", "Graduate"
        )

    def test_total_syllables(self):
        result = analyze_readability("Hello world")
        assert result["total_syllables"] > 0

    def test_avg_words_per_sentence(self):
        result = analyze_readability("One. Two. Three.")
        assert result["avg_words_per_sentence"] == 1.0

    def test_empty_text_handled(self):
        result = analyze_readability("12345")
        assert result["total_words"] >= 0

    def test_syllable_count(self):
        assert _count_syllables("the") == 1
        assert _count_syllables("hello") == 2
        assert _count_syllables("cat") == 1

    def test_reading_ease_bounds(self):
        result = analyze_readability("The quick brown fox jumps over the lazy dog.")
        assert 0 <= result["flesch_reading_ease"] <= 100

    def test_grade_positive(self):
        result = analyze_readability("This is a test sentence for readability analysis.")
        assert result["flesch_kincaid_grade"] >= 0
