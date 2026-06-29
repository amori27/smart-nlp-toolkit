"""Tests for language detection."""

import pytest
from app.services.language import detect_language


class TestLanguageDetection:
    def test_english(self):
        result = detect_language("The quick brown fox jumps over the lazy dog")
        assert result["language"] == "en"
        assert result["confidence"] > 0.3

    def test_arabic(self):
        result = detect_language("مرحبا بك في العالم العربي")
        assert result["language"] == "ar"
        assert result["confidence"] > 0.3

    def test_spanish(self):
        result = detect_language("El gato está en la mesa y es muy bonito")
        assert result["language"] == "es"
        assert result["confidence"] > 0.2

    def test_french(self):
        result = detect_language("Le chat est sur la table et il est très beau")
        assert result["language"] == "fr"
        assert result["confidence"] > 0.2

    def test_german(self):
        result = detect_language("Der Hund ist im Garten und er ist sehr groß")
        assert result["language"] == "de"
        assert result["confidence"] > 0.2

    def test_chinese(self):
        result = detect_language("这是一个中文句子的测试")
        assert result["language"] == "zh"
        assert result["confidence"] > 0.3

    def test_empty_candidates_for_symbols_only(self):
        result = detect_language("12345 !!! ???")
        assert result["language"] == "unknown"

    def test_candidates_structure(self):
        result = detect_language("Hello world")
        assert "candidates" in result
        assert len(result["candidates"]) <= 5
        for c in result["candidates"]:
            assert "language" in c
            assert "confidence" in c
