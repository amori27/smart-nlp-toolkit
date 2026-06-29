"""Tests for entity extraction."""

import pytest
from app.services.entities import extract_entities


class TestEntityExtraction:
    def test_email(self):
        ents = extract_entities("Contact us at hello@example.com for details")
        types = [e.type.value for e in ents]
        assert "email" in types
        assert any(e.value == "hello@example.com" for e in ents)

    def test_url(self):
        ents = extract_entities("Visit https://www.example.com/page?q=1 now")
        types = [e.type.value for e in ents]
        assert "url" in types

    def test_phone(self):
        ents = extract_entities("Call me at +1 555-123-4567 today")
        types = [e.type.value for e in ents]
        assert "phone" in types

    def test_hashtag(self):
        ents = extract_entities("This is #awesome and #great stuff")
        values = [e.value for e in ents]
        assert "#awesome" in values
        assert "#great" in values

    def test_date(self):
        ents = extract_entities("The event is on 2024-01-15")
        types = [e.type.value for e in ents]
        assert "date" in types

    def test_amount(self):
        ents = extract_entities("It costs $99.99 plus tax")
        types = [e.type.value for e in ents]
        assert "amount" in types

    def test_multiple_types(self):
        text = "Email john@test.com or call +1-555-1234, visit https://example.com, pay $50 on 2024-03-15 #launch"
        ents = extract_entities(text)
        types = {e.type.value for e in ents}
        assert types == {"email", "phone", "url", "amount", "date", "hashtag"}

    def test_empty_text(self):
        ents = extract_entities("no entities here just words")
        assert ents == []

    def test_entity_has_positions(self):
        ents = extract_entities("test@example.com")
        assert ents[0].start < ents[0].end

    def test_no_overlap(self):
        text = "test@example.com" * 3
        ents = extract_entities(text)
        for i in range(len(ents) - 1):
            assert ents[i].end <= ents[i + 1].start
