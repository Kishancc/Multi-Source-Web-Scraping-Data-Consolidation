from processing.deduplication import (
    normalize_text,
    create_duplicate_key,
    deduplicate_records,
)


def make_record(
    title,
    source="books.toscrape.com",
    author=""
):
    return {
        "source": source,
        "source_url": "https://example.com/test",
        "name_or_title": title,
        "category": "",
        "price": 10.0,
        "rating": 4,
        "author": author,
        "tags": "",
        "description": "",
        "scraped_at": "2026-10-06T12:00:00+00:00",
    }


def test_normalize_text():
    assert normalize_text(
        "  The   Great   Book  "
    ) == "the great book"


def test_duplicate_keys():
    record1 = make_record("The Great Book")
    record2 = make_record("  THE   GREAT BOOK ")

    assert create_duplicate_key(record1) == create_duplicate_key(record2)


def test_different_sources_are_not_duplicates():
    record1 = make_record(
        "The Great Book",
        source="books.toscrape.com"
    )

    record2 = make_record(
        "The Great Book",
        source="quotes.toscrape.com"
    )

    assert create_duplicate_key(record1) != create_duplicate_key(record2)


def test_deduplicate_records():
    record1 = make_record("The Great Book")
    record2 = make_record("  THE GREAT BOOK  ")
    record3 = make_record("Another Book")

    unique, duplicates = deduplicate_records(
        [record1, record2, record3]
    )

    assert len(unique) == 2
    assert len(duplicates) == 1

    assert unique[0]["name_or_title"] == "The Great Book"
    assert unique[1]["name_or_title"] == "Another Book"