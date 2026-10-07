# Web Scraping Assignment

A Python web scraping pipeline that collects data from two public practice websites, cleans and validates the data, removes duplicates, and produces consolidated output files.

## Websites Scraped

1. Books to Scrape
   - https://books.toscrape.com/
   - 1,000 book records collected
   - Supports pagination across all available book pages

2. Quotes to Scrape
   - https://quotes.toscrape.com/
   - 100 quote records collected
   - Supports pagination across all available quote pages

## Features

- HTTP requests using `requests`
- HTML parsing using BeautifulSoup
- `lxml` parser
- Pagination handling
- Request timeout handling
- Automatic retries for temporary HTTP errors
- Custom User-Agent
- Logging
- Unicode-safe text handling
- Data cleaning
- Data validation
- Duplicate detection and removal
- CSV output
- JSON summary report
- Automated tests using pytest

## Project Structure

```text
scraping_assignment/
│
├── scrapers/
│   ├── __init__.py
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── processing/
│   ├── __init__.py
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── tests/
│   ├── conftest.py
│   ├── test_base_scraper.py
│   ├── test_books_scraper.py
│   ├── test_quotes_scraper.py
│   ├── test_cleaning.py
│   ├── test_validation.py
│   └── test_deduplication.py
│
├── output/
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── logs/
│   └── scraping.log
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md
```

## Requirements

- Python 3.11+
- Internet connection
- pip

## Installation

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the Scraper

From the project root:

```powershell
python main.py
```

The pipeline performs the following steps:

```text
Scraping
   ↓
Cleaning
   ↓
Validation
   ↓
Deduplication
   ↓
CSV + JSON output
```

## Data Schema

The consolidated dataset contains the following fields:

| Field | Description |
|---|---|
| `source` | Website from which the record was collected |
| `source_url` | URL associated with the scraped record |
| `name_or_title` | Book title or quote text |
| `category` | Category when available |
| `price` | Book price when available |
| `rating` | Book rating from 1 to 5 when available |
| `author` | Quote author when available |
| `tags` | Quote tags when available |
| `description` | Description when available |
| `scraped_at` | UTC timestamp when the record was scraped |

Fields that are not available on a particular source are left empty.

## Data Cleaning

The cleaning stage:

- Removes leading and trailing whitespace
- Normalizes repeated whitespace
- Converts prices into numeric values
- Converts ratings into integer values
- Normalizes tags
- Handles missing values
- Preserves Unicode characters

## Data Validation

Records are validated for:

- Required fields
- Valid HTTP/HTTPS source URLs
- Numeric prices
- Non-negative prices
- Ratings between 1 and 5

Invalid records are separated and reported rather than silently included in the final dataset.

## Deduplication

Duplicate records are detected using normalized values based on:

- Source
- Title/text
- Author

The first occurrence is retained and subsequent duplicate records are removed.

## Error Handling

The scraper includes:

- Request timeouts
- HTTP error handling
- Retry logic for temporary failures
- Logging of failed requests
- Parser-level exception handling
- Pipeline-level exception handling

If a page request fails, the failure is logged and the pipeline handles the error without silently hiding it.

## Logging

Execution logs are written to:

```text
logs/scraping.log
```

Logs include:

- URLs being requested
- HTTP status codes
- Number of records found per page
- Parsing errors
- Validation results
- Duplicate counts
- Output file locations
- Pipeline completion status

## Output

### CSV

```text
output/final_dataset.csv
```

Contains the final cleaned, validated, and deduplicated dataset.

### JSON Summary

```text
output/summary_report.json
```

Contains:

- Total scraped records
- Cleaned records
- Rejected records
- Duplicate records
- Final record count
- Per-source statistics
- Execution time
- Generation timestamp

## Test Suite

Tests are implemented using `pytest`.

Run:

```powershell
pytest -v
```

### Latest Test Result

```text
20 passed
```

The test suite covers:

- Base scraper
- Books scraper
- Quotes scraper
- Text cleaning
- Price cleaning
- Rating cleaning
- Tag cleaning
- Record cleaning
- URL validation
- Record validation
- Deduplication

## Latest Scraping Results

The latest successful execution produced:

| Metric | Result |
|---|---:|
| Books scraped | 1,000 |
| Quotes scraped | 100 |
| Total records scraped | 1,100 |
| Records after cleaning | 1,100 |
| Valid records | 1,100 |
| Rejected records | 0 |
| Duplicate records | 1 |
| Final unique records | 1,099 |
| Tests passed | 20 |
| Pipeline execution time | ~85 seconds |

## AI Usage

AI assistance was used during development for planning, implementation guidance, debugging, testing ideas, and documentation.

Details are provided separately in:

```text
AI_USAGE.md
```

The implementation was manually reviewed and executed locally, and the final scraper and outputs were verified through automated tests and an actual scraping run.

## Notes

The project is intended for educational/practice purposes using publicly available scraping websites.

The scraper uses a delay between requests and does not attempt to bypass website restrictions or authentication.
