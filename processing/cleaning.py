import re


def clean_text(value):
    """
    Normalize text by removing extra whitespace.

    Missing values are converted to an empty string.
    """

    if value is None:
        return ""

    value = str(value)

    # Replace multiple whitespace characters with one space
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def clean_price(value):
    """
    Convert a price such as '£51.77' into a numeric float.

    Invalid or missing values return None.
    """

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # Keep digits and decimal point
    cleaned = re.sub(r"[^0-9.]", "", value)

    if not cleaned:
        return None

    try:
        return float(cleaned)

    except ValueError:
        return None


def clean_rating(value):
    """
    Convert rating values into integers from 1 to 5.

    Invalid values return None.
    """

    if value is None:
        return None

    try:
        rating = int(value)

    except (TypeError, ValueError):
        return None

    if 1 <= rating <= 5:
        return rating

    return None


def clean_tags(value):
    """
    Normalize tags into a comma-separated string.
    """

    if value is None:
        return ""

    if isinstance(value, list):
        tags = [
            clean_text(tag)
            for tag in value
            if clean_text(tag)
        ]

        return ", ".join(tags)

    return clean_text(value)


def clean_record(record):
    """
    Clean one standardized scraper record.
    """

    cleaned = record.copy()

    cleaned["source"] = clean_text(
        cleaned.get("source")
    )

    cleaned["source_url"] = clean_text(
        cleaned.get("source_url")
    )

    cleaned["name_or_title"] = clean_text(
        cleaned.get("name_or_title")
    )

    cleaned["category"] = clean_text(
        cleaned.get("category")
    )

    cleaned["price"] = clean_price(
        cleaned.get("price")
    )

    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )

    cleaned["author"] = clean_text(
        cleaned.get("author")
    )

    cleaned["tags"] = clean_tags(
        cleaned.get("tags")
    )

    cleaned["description"] = clean_text(
        cleaned.get("description")
    )

    cleaned["scraped_at"] = clean_text(
        cleaned.get("scraped_at")
    )

    return cleaned


def clean_records(records):
    """
    Clean a list of scraper records.
    """

    return [
        clean_record(record)
        for record in records
    ]