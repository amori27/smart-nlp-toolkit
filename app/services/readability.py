"""Flesch-Kincaid readability scoring."""

from __future__ import annotations

import re


def _count_syllables(word: str) -> int:
    """Estimate syllable count for a single English word."""
    word = word.lower()
    if len(word) <= 2:
        return 1
    word = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", word)
    word = re.sub(r"^y", "", word)
    vowels = re.findall(r"[aeiouy]+", word)
    count = len(vowels)
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def _split_sentences(text: str) -> list[str]:
    raw = re.split(r"(?<=[.!?])\s+", text)
    return [s for s in raw if s.strip()]


def _get_words(text: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z]+\b", text)


def analyze_readability(text: str) -> dict:
    """
    Compute Flesch-Kincaid Grade Level and Reading Ease scores.

    Returns dict with scores, averages, totals, and reading level interpretation.
    """
    sentences = _split_sentences(text)
    words = _get_words(text)

    num_sentences = max(len(sentences), 1)
    num_words = max(len(words), 1)
    total_syllables = sum(_count_syllables(w) for w in words)

    avg_wps = num_words / num_sentences
    avg_spw = total_syllables / num_words

    # Flesch Reading Ease (higher = easier to read)
    flesch_ease = (
        206.835 - (1.015 * avg_wps) - (84.6 * avg_spw)
    )
    flesch_ease = round(max(0, min(100, flesch_ease)), 2)

    # Flesch-Kincaid Grade Level
    flesch_grade = 0.39 * avg_wps + 11.8 * avg_spw - 15.59
    flesch_grade = round(max(0, flesch_grade), 2)

    # Interpret reading level
    if flesch_grade <= 5:
        level = "Elementary"
    elif flesch_grade <= 8:
        level = "Middle School"
    elif flesch_grade <= 12:
        level = "High School"
    elif flesch_grade <= 16:
        level = "College"
    else:
        level = "Graduate"

    return {
        "flesch_kincaid_grade": flesch_grade,
        "flesch_reading_ease": flesch_ease,
        "avg_words_per_sentence": round(avg_wps, 2),
        "avg_syllables_per_word": round(avg_spw, 2),
        "total_words": num_words,
        "total_sentences": num_sentences,
        "total_syllables": total_syllables,
        "level": level,
    }
