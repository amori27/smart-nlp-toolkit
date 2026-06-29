"""Extractive summarization using TF-inspired sentence scoring."""

from __future__ import annotations

import math
import re
from collections import Counter


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences, handling common abbreviations."""
    # Protect abbreviations
    protected = text
    abbrevs = ["Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "vs.", "etc.", "e.g.", "i.e."]
    for abbr in abbrevs:
        protected = protected.replace(abbr, abbr.replace(".", "<<DOT>>"))

    raw = re.split(r"(?<=[.!?])\s+", protected)
    sentences = [s.replace("<<DOT>>", ".") for s in raw if len(s.strip()) > 10]
    return sentences


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokenizer."""
    return re.findall(r"\b\w+\b", text.lower())


def _word_freq(tokens: list[str]) -> Counter:
    """Compute word frequencies, excluding common stop words."""
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "into", "through", "during",
        "before", "after", "above", "below", "between", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "each", "every", "both", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "just", "about", "and", "but",
        "or", "if", "while", "that", "this", "these", "those", "it", "its",
        "i", "me", "my", "we", "our", "you", "your", "he", "him", "his",
        "she", "her", "they", "them", "their", "what", "which", "who", "whom",
    }
    return Counter(w for w in tokens if w not in stopwords and len(w) > 1)


def summarize_text(text: str, num_sentences: int = 3) -> dict:
    """
    Extractive summarization: score sentences by word frequency
    and return the top *num_sentences* most important ones.

    Returns a dict with summary, lengths, and compression ratio.
    """
    sentences = _split_sentences(text)
    if len(sentences) <= num_sentences:
        joined = " ".join(sentences)
        return {
            "summary": joined,
            "original_length": len(text),
            "summary_length": len(joined),
            "compression_ratio": round(len(joined) / max(len(text), 1), 4),
            "num_sentences_original": len(sentences),
            "num_sentences_summary": len(sentences),
        }

    all_tokens = _tokenize(text)
    freq = _word_freq(all_tokens)
    if not freq:
        return {
            "summary": sentences[0],
            "original_length": len(text),
            "summary_length": len(sentences[0]),
            "compression_ratio": round(len(sentences[0]) / max(len(text), 1), 4),
            "num_sentences_original": len(sentences),
            "num_sentences_summary": 1,
        }

    max_freq = max(freq.values())

    scored: list[tuple[int, float]] = []
    for idx, sentence in enumerate(sentences):
        tokens = _tokenize(sentence)
        if not tokens:
            scored.append((idx, 0.0))
            continue
        score = sum(freq.get(w, 0) for w in tokens) / len(tokens)
        # Boost first sentences (position bias — leads with topic)
        if idx < 2:
            score *= 1.2
        scored.append((idx, score))

    top_indices = sorted(
        [idx for idx, _ in sorted(scored, key=lambda x: -x[1])[:num_sentences]]
    )
    summary_sentences = [sentences[i] for i in top_indices]
    joined = " ".join(summary_sentences)

    return {
        "summary": joined,
        "original_length": len(text),
        "summary_length": len(joined),
        "compression_ratio": round(len(joined) / max(len(text), 1), 4),
        "num_sentences_original": len(sentences),
        "num_sentences_summary": len(summary_sentences),
    }
