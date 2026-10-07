import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

from processing.cleaning import clean_records
from processing.validation import validate_records
from processing.deduplication import deduplicate_records


# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

LOG_FILE = LOG_DIR / "scraping.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Scraping
# -------------------------------------------------------------------

def scrape_all():
    """
    Run all scrapers and return raw records by source.
    """

    logger.info("Starting scraping pipeline")

    books_scraper = BooksScraper(delay=0.5)
    quotes_scraper = QuotesScraper(delay=0.5)

    books = books_scraper.scrape()
    quotes = quotes_scraper.scrape()

    logger.info(
        "Books records collected: %d",
        len(books)
    )

    logger.info(
        "Quotes records collected: %d",
        len(quotes)
    )

    return {
        "books.toscrape.com": books,
        "quotes.toscrape.com": quotes,
    }


# -------------------------------------------------------------------
# CSV output
# -------------------------------------------------------------------

def write_csv(records, output_file):
    """
    Write standardized records to CSV.
    """

    import csv

    fieldnames = [
        "source",
        "source_url",
        "name_or_title",
        "category",
        "price",
        "rating",
        "author",
        "tags",
        "description",
        "scraped_at",
    ]

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for record in records:
            writer.writerow(record)


# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------

def build_summary(
    raw_records,
    cleaned_records,
    rejected_records,
    duplicate_records,
    final_records,
    execution_time,
):
    """
    Build the JSON summary report.
    """

    source_summary = {}

    for source, records in raw_records.items():

        source_cleaned = [
            record
            for record in cleaned_records
            if record.get("source") == source
        ]

        source_rejected = [
            item
            for item in rejected_records
            if item["record"].get("source") == source
        ]

        source_duplicates = [
            record
            for record in duplicate_records
            if record.get("source") == source
        ]

        source_final = [
            record
            for record in final_records
            if record.get("source") == source
        ]

        source_summary[source] = {
            "scraped": len(records),
            "cleaned": len(source_cleaned),
            "rejected": len(source_rejected),
            "duplicates": len(source_duplicates),
            "final": len(source_final),
        }

    return {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "execution_time_seconds": round(
            execution_time,
            2
        ),

        "total_scraped": sum(
            len(records)
            for records in raw_records.values()
        ),

        "total_cleaned": len(cleaned_records),

        "total_rejected": len(
            rejected_records
        ),

        "total_duplicates": len(
            duplicate_records
        ),

        "final_record_count": len(
            final_records
        ),

        "sources": source_summary,
    }


# -------------------------------------------------------------------
# Main pipeline
# -------------------------------------------------------------------

def main():

    start_time = time.perf_counter()

    try:

        # -----------------------------------------------------------
        # 1. Scrape
        # -----------------------------------------------------------

        raw_records = scrape_all()

        all_raw_records = []

        for records in raw_records.values():
            all_raw_records.extend(records)

        logger.info(
            "Total raw records: %d",
            len(all_raw_records)
        )

        # -----------------------------------------------------------
        # 2. Clean
        # -----------------------------------------------------------

        cleaned_records = clean_records(
            all_raw_records
        )

        logger.info(
            "Records after cleaning: %d",
            len(cleaned_records)
        )

        # -----------------------------------------------------------
        # 3. Validate
        # -----------------------------------------------------------

        valid_records, rejected_records = (
            validate_records(
                cleaned_records
            )
        )

        logger.info(
            "Valid records: %d",
            len(valid_records)
        )

        logger.info(
            "Rejected records: %d",
            len(rejected_records)
        )

        # -----------------------------------------------------------
        # 4. Deduplicate
        # -----------------------------------------------------------

        unique_records, duplicate_records = (
            deduplicate_records(
                valid_records
            )
        )

        logger.info(
            "Unique records: %d",
            len(unique_records)
        )

        logger.info(
            "Duplicate records: %d",
            len(duplicate_records)
        )

        # -----------------------------------------------------------
        # 5. CSV
        # -----------------------------------------------------------

        csv_file = OUTPUT_DIR / "final_dataset.csv"

        write_csv(
            unique_records,
            csv_file
        )

        logger.info(
            "CSV written to: %s",
            csv_file
        )

        # -----------------------------------------------------------
        # 6. JSON summary
        # -----------------------------------------------------------

        execution_time = (
            time.perf_counter() - start_time
        )

        summary = build_summary(
            raw_records=raw_records,
            cleaned_records=cleaned_records,
            rejected_records=rejected_records,
            duplicate_records=duplicate_records,
            final_records=unique_records,
            execution_time=execution_time,
        )

        summary_file = (
            OUTPUT_DIR / "summary_report.json"
        )

        with open(
            summary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4
            )

        logger.info(
            "Summary written to: %s",
            summary_file
        )

        logger.info(
            "Pipeline completed successfully in %.2f seconds",
            execution_time
        )

    except Exception:
        logger.exception(
            "Pipeline failed unexpectedly"
        )
        raise


if __name__ == "__main__":
    main()