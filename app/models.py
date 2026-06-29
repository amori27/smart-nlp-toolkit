"""Pydantic v2 request and response models with full validation."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class EntityType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    HASHTAG = "hashtag"
    DATE = "date"
    AMOUNT = "amount"


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------

class TextInput(BaseModel):
    """Standard request body — every analysis endpoint accepts this."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=50_000,
        description="The text to analyze. Must be 1–50 000 characters.",
        examples=["The restaurant had amazing food but terrible service."],
    )

    @field_validator("text")
    @classmethod
    def text_must_contain_alphabetic(cls, v: str) -> str:
        if not any(c.isalpha() for c in v):
            raise ValueError(
                "Text must contain at least one alphabetic character."
            )
        return v.strip()


# ---------------------------------------------------------------------------
# Sentiment
# ---------------------------------------------------------------------------

class SentimentResponse(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(
        ge=0.0, le=1.0, description="Model confidence between 0 and 1."
    )
    scores: dict[str, float] = Field(
        description="Per-class probability scores."
    )


# ---------------------------------------------------------------------------
# Language
# ---------------------------------------------------------------------------

class LanguageResponse(BaseModel):
    language: str = Field(description="ISO 639-1 language code (e.g. 'en', 'ar').")
    confidence: float = Field(ge=0.0, le=1.0)
    candidates: list[dict[str, Any]] = Field(
        description="Top candidate languages with scores."
    )


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

class Entity(BaseModel):
    type: EntityType
    value: str
    start: int
    end: int


class EntitiesResponse(BaseModel):
    entities: list[Entity]
    count: int


# ---------------------------------------------------------------------------
# Summarization
# ---------------------------------------------------------------------------

class SummaryResponse(BaseModel):
    summary: str
    original_length: int = Field(description="Number of characters in the input.")
    summary_length: int = Field(description="Number of characters in the summary.")
    compression_ratio: float = Field(
        description="summary_length / original_length."
    )
    num_sentences_original: int
    num_sentences_summary: int


# ---------------------------------------------------------------------------
# Readability
# ---------------------------------------------------------------------------

class ReadabilityResponse(BaseModel):
    flesch_kincaid_grade: float
    flesch_reading_ease: float
    avg_words_per_sentence: float
    avg_syllables_per_word: float
    total_words: int
    total_sentences: int
    total_syllables: int
    level: str = Field(
        description="Reading level interpretation (e.g. 'College')."
    )


# ---------------------------------------------------------------------------
# Full analysis (single-call)
# ---------------------------------------------------------------------------

class FullAnalysisResponse(BaseModel):
    text_length: int
    word_count: int
    sentence_count: int
    sentiment: SentimentResponse
    language: LanguageResponse
    entities: EntitiesResponse
    readability: ReadabilityResponse
    summary: SummaryResponse
