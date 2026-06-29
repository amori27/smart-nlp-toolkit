"""Rule-based language detection using Unicode block + stop-word scoring."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

# ---------------------------------------------------------------------------
# Character-range heuristics for common scripts
# ---------------------------------------------------------------------------
_SCRIPT_RANGES: list[tuple[str, re.Pattern]] = [
    ("ar", re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")),
    ("zh", re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF]")),
    ("ja", re.compile(r"[\u3040-\u309F\u30A0-\u30FF]")),
    ("ko", re.compile(r"[\uAC00-\uD7AF\u1100-\u11FF]")),
    ("hi", re.compile(r"[\u0900-\u097F]")),
    ("ru", re.compile(r"[\u0400-\u04FF]")),
    ("th", re.compile(r"[\u0E00-\u0E7F]")),
    ("el", re.compile(r"[\u0370-\u03FF]")),
]

# ---------------------------------------------------------------------------
# Stop-word lists for disambiguation
# ---------------------------------------------------------------------------
_STOPWORDS: dict[str, set[str]] = {
    "en": {
        "the", "is", "at", "which", "on", "and", "a", "to", "in", "of",
        "for", "with", "it", "as", "be", "was", "are", "this", "that",
        "from", "by", "not", "or", "but", "have", "has", "had", "they",
        "we", "you", "he", "she", "its", "my", "your", "our", "will",
        "would", "can", "could", "should", "may", "do", "does", "did",
        "been", "being", "an", "if", "no", "so", "than", "then", "there",
        "here", "what", "when", "where", "how", "all", "each", "every",
        "about", "up", "out", "just", "more", "also", "very", "often",
    },
    "es": {
        "el", "la", "los", "las", "de", "del", "en", "y", "que", "un",
        "una", "por", "con", "para", "es", "son", "fue", "ser", "esta",
        "como", "más", "pero", "su", "al", "no", "se", "lo", "ya", "o",
        "este", "todo", "tiene", "han", "le", "ni", "sí", "sobre",
    },
    "fr": {
        "le", "la", "les", "de", "des", "en", "et", "un", "une", "que",
        "est", "qui", "dans", "pour", "sur", "pas", "avec", "son", "ses",
        "au", "aux", "ce", "cette", "il", "elle", "nous", "vous", "ils",
        "ne", "mais", "ou", "donc", "ni", "car", "par", "plus", "tout",
    },
    "de": {
        "der", "die", "das", "und", "in", "ist", "ein", "eine", "von",
        "den", "mit", "auf", "für", "des", "nicht", "sich", "auch", "als",
        "noch", "nach", "wie", "wird", "hat", "haben", "werden", "kann",
        "zur", "zum", "dem", "bei", "nur", "oder", "aber", "so", "sehr",
    },
    "pt": {
        "o", "a", "os", "as", "de", "do", "da", "em", "que", "um",
        "uma", "para", "com", "não", "uma", "por", "mais", "dos", "das",
        "seu", "sua", "seus", "suas", "ou", "ser", "quando", "muito",
        "nos", "já", "eu", "também", "só", "pelo", "pela", "até",
    },
    "it": {
        "il", "lo", "la", "le", "gli", "di", "del", "della", "in", "e",
        "un", "una", "che", "per", "con", "non", "si", "è", "sono",
        "questo", "questa", "ma", "anche", "suo", "sua", "più", "nel",
        "nella", "dal", "dalla", "su", "sul", "sulla", "o", "se",
    },
    "tr": {
        "bir", "ve", "bu", "bu", "için", "ile", "ne", "de", "da",
        "bu", "olarak", "bu", "en", "ancak", "veya", "gibi", "ki",
        "ben", "sen", "o", "biz", "siz", "onlar", "çok", "içinde",
        "daha", "kadar", "hem", "diye", "arasında", "üzerinde", "hangi",
    },
    "id": {
        "yang", "dan", "untuk", "dengan", "pada", "ke", "di", "ini",
        "itu", "adalah", "tidak", "akan", "juga", "sudah", "oleh",
        "atau", "dari", "dalam", "bisa", "lebih", "karena", "saat",
        "mereka", "kita", "ada", "apa", "bagi", "mau",
    },
    "nl": {
        "de", "het", "een", "van", "en", "in", "is", "dat", "op", "te",
        "voor", "met", "zijn", "niet", "ook", "aan", "hij", "zij", "als",
        "maar", "door", "was", "nog", "wel", "dit", "dat", "wordt",
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _script_score(text: str) -> dict[str, float]:
    """Score each script by proportion of matching characters."""
    total_alpha = sum(1 for c in text if c.isalpha())
    if total_alpha == 0:
        return {}
    scores: dict[str, float] = {}
    for lang, pattern in _SCRIPT_RANGES:
        matches = len(pattern.findall(text))
        scores[lang] = matches / total_alpha
    return scores


def _stopword_score(text: str) -> dict[str, float]:
    """Score languages by stop-word overlap."""
    words = set(re.findall(r"\b[a-zA-ZàâäéèêëïîôùûüÿçÀÂÄÉÈÊËÏÎÔÙÛÜŸÇñÑ]+\b", text.lower()))
    if not words:
        return {}
    scores: dict[str, float] = {}
    for lang, stopwords in _STOPWORDS.items():
        overlap = len(words & stopwords)
        scores[lang] = overlap / len(words)
    return scores


def detect_language(text: str) -> dict:
    """
    Detect the most likely language of *text*.

    Returns dict with ``language``, ``confidence``, and ``candidates``.
    Uses script-range heuristics first, then stop-word overlap.
    """
    scores: dict[str, float] = {}

    # Script heuristics (strong signal for non-Latin scripts)
    script_scores = _script_score(text)
    for lang, score in script_scores.items():
        if score > 0.1:  # meaningful presence
            scores[lang] = score * 10  # boost script signal

    # Stop-word scoring (primary signal for Latin-script languages)
    sw_scores = _stopword_score(text)
    for lang, score in sw_scores.items():
        scores[lang] = scores.get(lang, 0.0) + score

    if not scores:
        return {
            "language": "unknown",
            "confidence": 0.0,
            "candidates": [],
        }

    # Normalize
    total = sum(scores.values())
    if total == 0:
        return {"language": "unknown", "confidence": 0.0, "candidates": []}

    normalized = {k: v / total for k, v in scores.items()}
    sorted_candidates = sorted(normalized.items(), key=lambda x: -x[1])

    top_lang, top_score = sorted_candidates[0]
    candidates = [{"language": lang, "confidence": round(conf, 4)} for lang, conf in sorted_candidates[:5]]

    return {
        "language": top_lang,
        "confidence": round(top_score, 4),
        "candidates": candidates,
    }
