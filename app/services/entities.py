"""Regex-based named-entity extraction."""

from __future__ import annotations

import re

from app.models import Entity, EntityType


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_PATTERNS: list[tuple[EntityType, re.Pattern]] = [
    (
        EntityType.EMAIL,
        re.compile(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
        ),
    ),
    (
        EntityType.URL,
        re.compile(
            r"https?://(?:www\.)?[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}(?:/[^\s)\]\},]*)?"
            r"|www\.[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}(?:/[^\s)\]\},]*)?"
        ),
    ),
    (
        EntityType.PHONE,
        re.compile(
            r"(?:\+\d{1,3}[\s\-]?)?"
            r"(?:\(?\d{2,4}\)?[\s\-]?)?"
            r"\d{3,4}[\s\-]?\d{3,4}"
            r"|\d{5,15}"
        ),
    ),
    (
        EntityType.HASHTAG,
        re.compile(r"#\w{2,}"),
    ),
    (
        EntityType.DATE,
        re.compile(
            r"(?:\d{1,4}[\-/.]\d{1,2}[\-/.]\d{1,4})"  # 2024-01-15
            r"|(?:\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
            r"(?:\w*\.?)\s+\d{1,4})"                     # 15 January 2024
            r"|(?:\d{1,2}\s+(?:January|February|March|April|May|June|July|"
            r"August|September|October|November|December)\s+\d{1,4})",
            re.IGNORECASE,
        ),
    ),
    (
        EntityType.AMOUNT,
        re.compile(
            r"\$[\d,]+(?:\.\d{2})?"
            r"|€[\d,]+(?:\.\d{2})?"
            r"|£[\d,]+(?:\.\d{2})?"
            r"|(?:USD|EUR|GBP)\s?\d[\d,.]*"
            r"|\d[\d,.]*\s*(?:USD|EUR|GBP|dollars|euros|pounds)"
            r"|\b\d[\d,.]*\s*(?:thousand|million|billion)\b",
            re.IGNORECASE,
        ),
    ),
]


def extract_entities(text: str) -> list[Entity]:
    """Return all entities found in *text*, sorted by position."""
    entities: list[Entity] = []
    used_spans: list[tuple[int, int]] = []

    for etype, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            # Skip overlapping matches
            if any(s < end and start < e for s, e in used_spans):
                continue
            entities.append(
                Entity(type=etype, value=match.group(), start=start, end=end)
            )
            used_spans.append((start, end))

    entities.sort(key=lambda e: e.start)
    return entities
