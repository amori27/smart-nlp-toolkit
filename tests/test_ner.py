"""Extended tests for named entity recognition (NER) edge cases."""

from app.models import EntityType
from app.services.entities import extract_entities


class TestNEREdgeCases:
    """Test entity extraction with complex and edge-case inputs."""

    def test_overlapping_entities_skip_later_match(self):
        """When two patterns match the same span, only the first is kept."""
        text = "Email: test@example.com"
        ents = extract_entities(text)
        email_ents = [e for e in ents if e.type == EntityType.EMAIL]
        assert len(email_ents) == 1
        assert email_ents[0].value == "test@example.com"

    def test_entities_sorted_by_start_position(self):
        text = "Call +1-555-0199 or email user@host.com"
        ents = extract_entities(text)
        starts = [e.start for e in ents]
        assert starts == sorted(starts)

    def test_positions_match_actual_text(self):
        text = "Pay $123.45 on 2024-06-01"
        ents = extract_entities(text)
        for e in ents:
            assert text[e.start : e.end] == e.value

    def test_email_with_plus_addressing(self):
        ents = extract_entities("Send to user+tag@gmail.com please")
        emails = [e.value for e in ents if e.type == EntityType.EMAIL]
        assert "user+tag@gmail.com" in emails

    def test_email_with_subdomain(self):
        ents = extract_entities("Contact mail@mail.example.co.uk")
        emails = [e.value for e in ents if e.type == EntityType.EMAIL]
        assert len(emails) == 1

    def test_url_www_prefix(self):
        ents = extract_entities("Visit www.example.com for info")
        urls = [e.value for e in ents if e.type == EntityType.URL]
        assert any("www.example.com" in v for v in urls)

    def test_url_http_only(self):
        ents = extract_entities("Go to http://insecure-site.org/path")
        urls = [e.value for e in ents if e.type == EntityType.URL]
        assert len(urls) == 1

    def test_phone_international_format(self):
        ents = extract_entities("Dial +44 20 7946 0958 for UK office")
        phones = [e for e in ents if e.type == EntityType.PHONE]
        assert len(phones) >= 1

    def test_hashtag_at_start_of_text(self):
        ents = extract_entities("#trending is the topic today")
        tags = [e.value for e in ents if e.type == EntityType.HASHTAG]
        assert "#trending" in tags

    def test_hashtag_with_underscore(self):
        ents = extract_entities("Check #my_topic and #another_one")
        tags = [e.value for e in ents if e.type == EntityType.HASHTAG]
        assert len(tags) == 2

    def test_date_with_text_month(self):
        ents = extract_entities("Born on 15 March 1990")
        dates = [e for e in ents if e.type == EntityType.DATE]
        assert len(dates) == 1

    def test_date_slash_separated(self):
        ents = extract_entities("Meeting on 03/15/2024 at noon")
        dates = [e for e in ents if e.type == EntityType.DATE]
        assert len(dates) == 1

    def test_amount_euro(self):
        ents = extract_entities("Price is €49.99")
        amounts = [e.value for e in ents if e.type == EntityType.AMOUNT]
        assert any("€49.99" in v for v in amounts)

    def test_amount_gbp(self):
        ents = extract_entities("Costs £120.00 total")
        amounts = [e.value for e in ents if e.type == EntityType.AMOUNT]
        assert len(amounts) >= 1

    def test_amount_with_currency_code(self):
        ents = extract_entities("Transfer USD 500 to the account")
        amounts = [e for e in ents if e.type == EntityType.AMOUNT]
        assert len(amounts) == 1

    def test_amount_million_words(self):
        ents = extract_entities("The project costs 5 million dollars")
        amounts = [e for e in ents if e.type == EntityType.AMOUNT]
        assert len(amounts) == 1

    def test_multiple_emails_no_overlap(self):
        text = "Send to a@b.com and c@d.com and e@f.com"
        ents = extract_entities(text)
        emails = [e for e in ents if e.type == EntityType.EMAIL]
        assert len(emails) == 3
        spans = [(e.start, e.end) for e in emails]
        for i in range(len(spans)):
            for j in range(i + 1, len(spans)):
                assert spans[i][1] <= spans[j][0] or spans[j][1] <= spans[i][0]

    def test_entity_type_enum_values(self):
        """Verify EntityType enum covers all expected types."""
        expected = {"email", "phone", "url", "hashtag", "date", "amount"}
        actual = {et.value for et in EntityType}
        assert expected == actual

    def test_empty_string_returns_empty(self):
        assert extract_entities("") == []

    def test_only_whitespace_returns_empty(self):
        assert extract_entities("   \n\t  ") == []
