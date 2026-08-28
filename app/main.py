"""Smart NLP Toolkit — FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.models import (
    EntitiesResponse,
    FullAnalysisResponse,
    LanguageResponse,
    ReadabilityResponse,
    SentimentResponse,
    SummaryResponse,
    TextInput,
)
from app.services import entities, language, readability, sentiment, summarizer

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "A production-grade NLP microservice for sentiment analysis, "
        "language detection, entity extraction, text summarization, "
        "and readability scoring — no external API keys required."
    ),
    contact={"name": "Amir Asaad", "email": "amirasaadprog@gmail.com"},
    license_info={"name": "MIT"},
)


# ---------------------------------------------------------------------------
# Custom exception handler for Pydantic validation errors
# ---------------------------------------------------------------------------
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Unprocessable Entity",
            "detail": str(exc),
        },
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


# ---------------------------------------------------------------------------
# Sentiment
# ---------------------------------------------------------------------------
@app.post("/sentiment", response_model=SentimentResponse, tags=["analysis"])
async def analyze_sentiment(body: TextInput):
    try:
        result = sentiment.classify_sentiment(body.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {exc}")
    return result


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------
@app.post("/language", response_model=LanguageResponse, tags=["analysis"])
async def detect_language_endpoint(body: TextInput):
    try:
        result = language.detect_language(body.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Language detection failed: {exc}")
    return result


# ---------------------------------------------------------------------------
# Entity extraction
# ---------------------------------------------------------------------------
@app.post("/entities", response_model=EntitiesResponse, tags=["analysis"])
async def extract_entities_endpoint(body: TextInput):
    try:
        found = entities.extract_entities(body.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {exc}")
    return EntitiesResponse(entities=found, count=len(found))


# ---------------------------------------------------------------------------
# Summarization
# ---------------------------------------------------------------------------
@app.post("/summarize", response_model=SummaryResponse, tags=["analysis"])
async def summarize_endpoint(body: TextInput, num_sentences: int = 3):
    try:
        result = summarizer.summarize_text(body.text, num_sentences=num_sentences)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}")
    return result


# ---------------------------------------------------------------------------
# Readability
# ---------------------------------------------------------------------------
@app.post("/readability", response_model=ReadabilityResponse, tags=["analysis"])
async def readability_endpoint(body: TextInput):
    try:
        result = readability.analyze_readability(body.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Readability analysis failed: {exc}")
    return result


# ---------------------------------------------------------------------------
# Full analysis (single-call)
# ---------------------------------------------------------------------------
@app.post("/analyze", response_model=FullAnalysisResponse, tags=["analysis"])
async def full_analysis(body: TextInput, num_sentences: int = 3):
    try:
        word_count = len(body.text.split())
        sentence_count = max(len(readability._split_sentences(body.text)), 1)

        sent = sentiment.classify_sentiment(body.text)
        lang = language.detect_language(body.text)
        ents = entities.extract_entities(body.text)
        read = readability.analyze_readability(body.text)
        summ = summarizer.summarize_text(body.text, num_sentences=num_sentences)

        return FullAnalysisResponse(
            text_length=len(body.text),
            word_count=word_count,
            sentence_count=sentence_count,
            sentiment=sent,
            language=lang,
            entities=EntitiesResponse(entities=ents, count=len(ents)),
            readability=read,
            summary=summ,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {exc}")
