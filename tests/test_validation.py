from processing.validation import (
    is_valid_url,
    validate_record,
    validate_records,
)


def make_valid_record():
    return {
        "source": "books.toscrape.com",
        "source_url": "https://books.toscrape.com/catalogue/test_1/index.html",
        "name_or_title": "Test Book",
        "category": "Fiction",
        "price": 25.50,
        "rating": 4,
        "author": "",
        "tags": "",
        "description": "",
        "scraped_at": "2026-10-06T12:00:00+00:00",
    }


def test_valid_url():
    assert is_valid_url(
        "https://books.toscrape.com/"
    )

    assert is_valid_url(
        "http://example.com/test"
    )


def test_invalid_url():
    assert not is_valid_url("")
    assert not is_valid_url("not-a-url")


def test_valid_record():
    record = make_valid_record()

    is_valid, errors = validate_record(record)

    assert is_valid
    assert errors == []


def test_missing_required_field():
    record = make_valid_record()

    record["name_or_title"] = ""

    is_valid, errors = validate_record(record)

    assert not is_valid
    assert "Missing required field: name_or_title" in errors


def test_invalid_price():
    record = make_valid_record()

    record["price"] = "twenty"

    is_valid, errors = validate_record(record)

    assert not is_valid
    assert "Price must be numeric" in errors


def test_negative_price():
    record = make_valid_record()

    record["price"] = -10

    is_valid, errors = validate_record(record)

    assert not is_valid
    assert "Price cannot be negative" in errors


def test_invalid_rating():
    record = make_valid_record()

    record["rating"] = 6

    is_valid, errors = validate_record(record)

    assert not is_valid
    assert "Rating must be between 1 and 5" in errors


def test_validate_records():
    valid_record = make_valid_record()

    invalid_record = make_valid_record()
    invalid_record["name_or_title"] = ""

    valid, rejected = validate_records(
        [valid_record, invalid_record]
    )

    assert len(valid) == 1
    assert len(rejected) == 1