"""Extended tests for language detection edge cases."""

from app.services.language import detect_language, _script_score, _stopword_score


class TestLanguageDetectionExtended:
    """Test language detection with additional languages and edge cases."""

    def test_japanese_hiragana(self):
        result = detect_language("これは日本語のテストです。今日はいい天気ですね。")
        assert result["language"] == "ja"
        assert result["confidence"] > 0.3

    def test_korean(self):
        result = detect_language("안녕하세요 오늘 날씨가 정말 좋습니다")
        assert result["language"] == "ko"
        assert result["confidence"] > 0.3

    def test_hindi(self):
        result = detect_language("यह एक हिंदी वाक्य है जो परीक्षण के लिए लिखा गया है")
        assert result["language"] == "hi"
        assert result["confidence"] > 0.3

    def test_russian(self):
        result = detect_language("Это тестовое предложение на русском языке для проверки")
        assert result["language"] == "ru"
        assert result["confidence"] > 0.3

    def test_greek(self):
        result = detect_language("Αυτό είναι ένα δοκιμαστικό ελληνικό πρόταση")
        assert result["language"] == "el"
        assert result["confidence"] > 0.3

    def test_portuguese(self):
        result = detect_language("O gato está na mesa e é muito bonito com a luz do sol")
        assert result["language"] == "pt"
        assert result["confidence"] > 0.2

    def test_italian(self):
        result = detect_language("Il gatto è sulla tavola e è molto bello con la luce del sole")
        assert result["language"] == "it"
        assert result["confidence"] > 0.2

    def test_turkish(self):
        result = detect_language("Bu çok güzel bir gün ve ben çok mutluyum bugün")
        assert result["language"] == "tr"
        assert result["confidence"] > 0.2

    def test_indonesian(self):
        result = detect_language("Ini adalah hari yang sangat indah dan saya sangat senang")
        assert result["language"] == "id"
        assert result["confidence"] > 0.2

    def test_dutch(self):
        result = detect_language("Het is een mooie dag vandaag en ik ben heel blij met het weer")
        assert result["language"] == "nl"
        assert result["confidence"] > 0.2

    def test_thai(self):
        result = detect_language("นี่คือประโยคทดสอบภาษาไทยที่เขียนขึ้นเพื่อทดสอบระบบ")
        assert result["language"] == "th"
        assert result["confidence"] > 0.3

    def test_confidence_between_zero_and_one(self):
        result = detect_language("The quick brown fox jumps over the lazy dog")
        assert 0.0 <= result["confidence"] <= 1.0

    def test_returns_language_key(self):
        result = detect_language("Bonjour le monde")
        assert "language" in result
        assert isinstance(result["language"], str)

    def test_candidates_limited_to_five(self):
        result = detect_language("This is a test sentence with many English words")
        assert len(result["candidates"]) <= 5

    def test_candidates_have_required_fields(self):
        result = detect_language("Testing language detection with some text")
        for candidate in result["candidates"]:
            assert "language" in candidate
            assert "confidence" in candidate
            assert isinstance(candidate["confidence"], float)

    def test_short_text_detection(self):
        result = detect_language("the")
        assert result["language"] == "en"

    def test_long_text_detection(self):
        long_text = (
            "The quick brown fox jumps over the lazy dog. "
            "This is a longer passage to test language detection with "
            "more context. The additional words help improve accuracy."
        ) * 3
        result = detect_language(long_text)
        assert result["language"] == "en"
        assert result["confidence"] > 0.3

    def test_script_score_non_latin(self):
        scores = _script_score("مرحبا بالعالم")
        assert scores.get("ar", 0) > 0.5

    def test_stopword_score_english(self):
        scores = _stopword_score("the cat is on the mat and it is sleeping")
        assert scores.get("en", 0) > 0.1

    def test_stopword_score_empty(self):
        scores = _stopword_score("12345 !!! ???")
        assert scores == {} or all(v == 0 for v in scores.values())

    def test_script_score_empty(self):
        scores = _script_score("")
        assert scores == {}
