"""Integration tests for FastAPI endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestHealthEndpoint:
    async def test_health(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["service"] == "Smart NLP Toolkit"


class TestSentimentEndpoint:
    async def test_sentiment(self, client):
        resp = await client.post("/sentiment", json={"text": "I love this!"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["sentiment"] in ("positive", "negative", "neutral")
        assert 0.0 <= data["confidence"] <= 1.0

    async def test_sentiment_empty(self, client):
        resp = await client.post("/sentiment", json={"text": ""})
        assert resp.status_code == 422

    async def test_sentiment_no_alphabetic(self, client):
        resp = await client.post("/sentiment", json={"text": "12345"})
        assert resp.status_code == 422


class TestLanguageEndpoint:
    async def test_language(self, client):
        resp = await client.post("/language", json={"text": "The quick brown fox"})
        assert resp.status_code == 200
        assert "language" in resp.json()


class TestEntitiesEndpoint:
    async def test_entities(self, client):
        resp = await client.post(
            "/entities",
            json={"text": "Email john@test.com, call +1-555-1234, visit https://example.com"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["count"] >= 2
        assert len(data["entities"]) == data["count"]


class TestSummarizeEndpoint:
    async def test_summarize(self, client):
        text = (
            "Artificial intelligence has transformed many industries. "
            "Healthcare providers use AI for diagnostics. "
            "Financial institutions rely on ML for fraud detection. "
            "Manufacturing plants deploy robots for quality control."
        )
        resp = await client.post("/summarize", json={"text": text})
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_length"] < data["original_length"]


class TestReadabilityEndpoint:
    async def test_readability(self, client):
        resp = await client.post(
            "/readability",
            json={"text": "The quick brown fox jumps over the lazy dog."},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["flesch_kincaid_grade"] > 0


class TestAnalyzeEndpoint:
    async def test_full_analysis(self, client):
        text = "I love AI! Contact me at hello@test.com or visit https://example.com."
        resp = await client.post("/analyze", json={"text": text})
        assert resp.status_code == 200
        data = resp.json()
        assert "sentiment" in data
        assert "language" in data
        assert "entities" in data
        assert "readability" in data
        assert "summary" in data
        assert data["word_count"] > 0

    async def test_text_length_limit(self, client):
        resp = await client.post("/analyze", json={"text": "x" * 50001})
        assert resp.status_code == 422
