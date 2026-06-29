# 🧠 Smart NLP Toolkit API

A **production-grade** FastAPI microservice for natural language processing — sentiment analysis, language detection, entity extraction, text summarization, and readability scoring. **Zero external API keys required**. Fully offline with trained ML models.

![CI](https://img.shields.io/github/actions/workflow/status/amori27/smart-nlp-toolkit/ci.yml?branch=main&style=flat-square&label=CI)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)
![Tests](https://img.shields.io/badge/Tests-30%2B-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## ✨ Features

| Feature | Method | Description |
|---|---|---|
| **Sentiment Analysis** | scikit-learn NaiveBayes + TF-IDF | Classify text as positive / negative / neutral with confidence scores |
| **Language Detection** | Unicode block + stop-word scoring | Detect 13+ languages (English, Arabic, Spanish, French, German, Chinese, Japanese, Korean, Hindi, Russian, Thai, Greek, Portuguese, Italian, Turkish, Indonesian, Dutch) |
| **Entity Extraction** | Regex patterns | Extract emails, phone numbers, URLs, hashtags, dates, and monetary amounts |
| **Text Summarization** | TF-based extractive scoring | Get key sentences from long text, configurable compression |
| **Readability Scoring** | Flesch-Kincaid algorithm | Grade level, reading ease, syllable analysis |
| **Full Analysis** | All-in-one endpoint | Run every analysis in a single API call |

---

## 🚀 Quick Start

### Option 1: Run locally with Python

```bash
# Clone the repo
git clone https://github.com/amori27/smart-nlp-toolkit.git
cd smart-nlp-toolkit

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Run with Docker

```bash
# Build and run
docker compose up --build

# Or just build
docker build -t smart-nlp-toolkit .
docker run -p 8000:8000 smart-nlp-toolkit
```

### Option 3: Run with Docker directly (no clone)

```bash
docker run -p 8000:8000 ghcr.io/amori27/smart-nlp-toolkit:latest
```

> The API will be available at **http://localhost:8000**

---

## 📖 API Reference

Base URL: `http://localhost:8000`

Interactive docs available at **http://localhost:8000/docs** (Swagger UI)

### `POST /sentiment` — Sentiment Analysis

Classify text as positive, negative, or neutral.

**Request:**
```json
{
  "text": "The restaurant had amazing food but terrible service."
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.7234,
  "scores": {
    "negative": 0.1234,
    "neutral": 0.1532,
    "positive": 0.7234
  }
}
```

---

### `POST /language` — Language Detection

Detect the language of the input text.

**Request:**
```json
{
  "text": "The quick brown fox jumps over the lazy dog"
}
```

**Response:**
```json
{
  "language": "en",
  "confidence": 0.8921,
  "candidates": [
    {"language": "en", "confidence": 0.8921},
    {"language": "fr", "confidence": 0.0312}
  ]
}
```

---

### `POST /entities` — Entity Extraction

Extract emails, phone numbers, URLs, hashtags, dates, and amounts.

**Request:**
```json
{
  "text": "Email john@test.com or call +1-555-1234. Visit https://example.com. Price: $49.99. Event on 2024-03-15. #launch"
}
```

**Response:**
```json
{
  "entities": [
    {"type": "email", "value": "john@test.com", "start": 6, "end": 19},
    {"type": "phone", "value": "+1-555-1234", "start": 31, "end": 42},
    {"type": "url", "value": "https://example.com", "start": 51, "end": 71},
    {"type": "amount", "value": "$49.99", "start": 81, "end": 87},
    {"type": "date", "value": "2024-03-15", "start": 99, "end": 109},
    {"type": "hashtag", "value": "#launch", "start": 111, "end": 118}
  ],
  "count": 6
}
```

---

### `POST /summarize` — Text Summarization

Extract the most important sentences from text.

**Request:**
```json
{
  "text": "Artificial intelligence has transformed many industries. Healthcare providers use AI for diagnostics and treatment planning. Financial institutions rely on machine learning for fraud detection. Manufacturing plants deploy robots powered by AI for quality control. Retail companies use recommendation systems to personalize shopping. Transportation networks optimize routes using predictive algorithms."
}
```

**Query parameter:** `?num_sentences=3` (default: 3)

**Response:**
```json
{
  "summary": "Artificial intelligence has transformed many industries. Healthcare providers use AI for diagnostics and treatment planning. Financial institutions rely on machine learning for fraud detection.",
  "original_length": 450,
  "summary_length": 180,
  "compression_ratio": 0.4,
  "num_sentences_original": 6,
  "num_sentences_summary": 3
}
```

---

### `POST /readability` — Readability Analysis

Get Flesch-Kincaid grade level and reading ease scores.

**Request:**
```json
{
  "text": "The quick brown fox jumps over the lazy dog. It was a sunny day and the birds were singing."
}
```

**Response:**
```json
{
  "flesch_kincaid_grade": 2.31,
  "flesch_reading_ease": 98.56,
  "avg_words_per_sentence": 8.0,
  "avg_syllables_per_word": 1.12,
  "total_words": 16,
  "total_sentences": 2,
  "total_syllables": 18,
  "level": "Elementary"
}
```

---

### `POST /analyze` — Full Analysis (All-in-One)

Run every analysis on your text in a single call.

**Request:**
```json
{
  "text": "I love this product! Contact support at help@company.com or visit https://company.com/help."
}
```

**Query parameter:** `?num_sentences=3` (default: 3)

**Response:**
```json
{
  "text_length": 82,
  "word_count": 13,
  "sentence_count": 2,
  "sentiment": {
    "sentiment": "positive",
    "confidence": 0.8521,
    "scores": {"negative": 0.0231, "neutral": 0.1248, "positive": 0.8521}
  },
  "language": {
    "language": "en",
    "confidence": 0.9432,
    "candidates": [{"language": "en", "confidence": 0.9432}]
  },
  "entities": {
    "entities": [
      {"type": "email", "value": "help@company.com", "start": 33, "end": 49},
      {"type": "url", "value": "https://company.com/help", "start": 60, "end": 83}
    ],
    "count": 2
  },
  "readability": {
    "flesch_kincaid_grade": 5.12,
    "flesch_reading_ease": 78.45,
    "avg_words_per_sentence": 6.5,
    "avg_syllables_per_word": 1.23,
    "total_words": 13,
    "total_sentences": 2,
    "total_syllables": 16,
    "level": "Middle School"
  },
  "summary": {
    "summary": "I love this product! Contact support at help@company.com or visit https://company.com/help.",
    "original_length": 82,
    "summary_length": 82,
    "compression_ratio": 1.0,
    "num_sentences_original": 2,
    "num_sentences_summary": 2
  }
}
```

---

### `GET /health` — Health Check

```json
{"status": "ok", "service": "Smart NLP Toolkit", "version": "1.0.0"}
```

---

## ⚠️ Errors You Might Encounter

| Error | HTTP Status | When It Happens | How to Fix |
|---|---|---|---|
| `"text must contain at least one alphabetic character"` | **422** | You sent only numbers or symbols (e.g. `"12345"`) | Include at least one letter in the `text` field |
| `"text must be at least 1 character"` | **422** | You sent an empty string `""` | Provide non-empty text |
| `"text must be at most 50000 characters"` | **422** | Your text exceeds 50,000 characters | Split into smaller chunks or truncate |
| `"field required"` | **422** | You forgot to send the `text` field in the JSON body | Ensure your request body is `{"text": "your text here"}` |
| `"Sentiment analysis failed"` | **500** | Internal ML model error (rare) | Restart the server and try again |
| `"Language detection failed"` | **500** | Internal processing error | Restart the server and try again |
| **Connection refused** | *N/A* | Server is not running | Start the server: `uvicorn app.main:app --reload` |
| **ModuleNotFoundError** | *N/A* | Missing dependencies | Run `pip install -r requirements.txt` |
| **Docker build fails** | *N/A* | Network issues or missing files | Check Dockerfile is present and run `docker compose build` |
| **Port 8000 already in use** | *N/A* | Another process is using port 8000 | Change the port: `uvicorn app.main:app --port 8001` or kill the conflicting process |
| **`language: "unknown"`** | *200* | Text has no recognizable language (only numbers/symbols) | Provide text with actual words in a known language |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.12** | Runtime |
| **FastAPI** | Web framework with automatic OpenAPI docs |
| **Pydantic v2** | Request/response validation and settings |
| **scikit-learn** | NaiveBayes sentiment classifier with TF-IDF |
| **Regex / Rule-based NLP** | Entity extraction, language detection, readability |
| **pytest + httpx** | Async integration tests |
| **Ruff** | Linting and formatting |
| **Docker** | Containerized deployment |
| **GitHub Actions** | CI/CD pipeline |

---

## 📁 Project Structure

```
smart-nlp-toolkit/
├── app/
│   ├── main.py              # FastAPI app, all routes
│   ├── models.py            # Pydantic v2 schemas (request/response)
│   ├── core/
│   │   └── config.py        # App settings via pydantic-settings
│   └── services/
│       ├── sentiment.py     # scikit-learn NB classifier
│       ├── language.py      # Unicode + stop-word language detection
│       ├── entities.py      # Regex entity extractor
│       ├── summarizer.py    # TF-based extractive summarization
│       └── readability.py   # Flesch-Kincaid readability scoring
├── tests/
│   ├── test_sentiment.py
│   ├── test_language.py
│   ├── test_entities.py
│   ├── test_summarizer.py
│   ├── test_readability.py
│   └── test_api.py          # Full API integration tests
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## 🧪 Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Lint
ruff check app/ tests/

# Auto-fix lint issues
ruff check --fix app/ tests/

# Run with hot reload
uvicorn app.main:app --reload
```

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Amir Asaad** — AI / Python Engineer

- 📧 amirasaadprog@gmail.com
- 🔗 [LinkedIn](https://linkedin.com/in/amir-asaad-7a1629377)
- 🐙 [GitHub](https://github.com/amori27)
