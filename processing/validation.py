from urllib.parse import urlparse


REQUIRED_FIELDS = [
    "source",
    "source_url",
    "name_or_title",
]


def is_valid_url(value):
    """
    Check whether a value is a valid HTTP/HTTPS URL.
    """

    if not value:
        return False

    try:
        parsed = urlparse(value)

        return parsed.scheme in {"http", "https"} and bool(
            parsed.netloc
        )

    except Exception:
        return False


def validate_record(record):
    """
    Validate one standardized record.

    Returns:
        tuple[bool, list[str]]
    """

    errors = []

    # Required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field)

        if value is None or str(value).strip() == "":
            errors.append(
                f"Missing required field: {field}"
            )

    # URL validation
    if record.get("source_url"):
        if not is_valid_url(record["source_url"]):
            errors.append(
                "Invalid source_url"
            )

    # Price validation
    price = record.get("price")

    if price is not None:
        if not isinstance(price, (int, float)):
            errors.append(
                "Price must be numeric"
            )
        elif price < 0:
            errors.append(
                "Price cannot be negative"
            )

    # Rating validation
    rating = record.get("rating")

    if rating is not None:
        if not isinstance(rating, int):
            errors.append(
                "Rating must be an integer"
            )
        elif not 1 <= rating <= 5:
            errors.append(
                "Rating must be between 1 and 5"
            )

    return len(errors) == 0, errors


def validate_records(records):
    """
    Validate multiple records.

    Returns:
        valid_records, rejected_records
    """

    valid_records = []
    rejected_records = []

    for record in records:
        is_valid, errors = validate_record(record)

        if is_valid:
            valid_records.append(record)
        else:
            rejected_records.append({
                "record": record,
                "errors": errors,
            })

    return valid_records, rejected_records