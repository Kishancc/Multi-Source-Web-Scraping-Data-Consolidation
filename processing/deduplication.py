import re


def normalize_text(value):
    """
    Normalize text for duplicate comparison.
    """

    if value is None:
        return ""

    value = str(value).strip().lower()

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value)

    return value


def create_duplicate_key(record):
    """
    Create a normalized key used to identify duplicate records.

    The source is included so that identical titles from
    different websites are not automatically considered duplicates.
    """

    source = normalize_text(record.get("source"))
    title = normalize_text(record.get("name_or_title"))
    author = normalize_text(record.get("author"))

    return (
        source,
        title,
        author,
    )


def deduplicate_records(records):
    """
    Remove duplicate records while preserving the first occurrence.

    Returns:
        unique_records, duplicate_records
    """

    seen = set()
    unique_records = []
    duplicate_records = []

    for record in records:
        key = create_duplicate_key(record)

        if key in seen:
            duplicate_records.append(record)
        else:
            seen.add(key)
            unique_records.append(record)

    return unique_records, duplicate_records