from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags,
    clean_record,
)


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"
    assert clean_text(None) == ""


def test_clean_price():
    assert clean_price("£51.77") == 51.77
    assert clean_price("$25.50") == 25.50
    assert clean_price("") is None
    assert clean_price(None) is None


def test_clean_rating():
    assert clean_rating(5) == 5
    assert clean_rating("3") == 3
    assert clean_rating(0) is None
    assert clean_rating(6) is None


def test_clean_tags():
    assert clean_tags(["fiction", "classic"]) == "fiction, classic"
    assert clean_tags(None) == ""


def test_clean_record():
    record = {
        "source": " books.toscrape.com ",
        "source_url": " https://example.com/book ",
        "name_or_title": "  Example   Book ",
        "category": "",
        "price": "£20.50",
        "rating": "4",
        "author": "",
        "tags": ["fiction", "classic"],
        "description": None,
        "scraped_at": " 2026-10-06 ",
    }

    cleaned = clean_record(record)

    assert cleaned["source"] == "books.toscrape.com"
    assert cleaned["name_or_title"] == "Example Book"
    assert cleaned["price"] == 20.50
    assert cleaned["rating"] == 4
    assert cleaned["tags"] == "fiction, classic"