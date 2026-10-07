# AI Usage Documentation

## AI Tool Used

**Tool:** ChatGPT

## Purpose of AI Assistance

AI was used only as a limited development assistant during this assignment.

It was mainly used for:

- Clarifying Python and BeautifulSoup concepts
- Getting guidance on pagination handling
- Debugging a few implementation issues
- Suggesting basic pytest test cases
- Reviewing documentation structure

The majority of the implementation was developed, tested, and verified manually.

## Representative Prompts

A few examples of prompts used were:

> "How can I handle pagination using BeautifulSoup?"

> "Help me debug this Python scraping error."

> "Suggest a few pytest test cases for this scraper."

> "How can I validate and clean scraped records?"

## AI-Assisted Parts

Limited AI assistance was used for:

- Pagination logic guidance
- Error-handling suggestions
- Data cleaning and validation ideas
- Test-case suggestions
- Minor debugging assistance

No complete application was directly copied from AI. The code was implemented and adapted based on the actual website structure.

## Changes After Reviewing AI Suggestions

AI suggestions were reviewed and modified where necessary.

One important correction involved Unicode encoding. After checking the generated CSV, the scraper was updated to use:

```python
response.encoding = response.apparent_encoding
```

This ensured that Unicode characters in scraped text were preserved correctly.

Another adjustment was made to avoid unnecessary detail-page requests, which reduced scraping time.

## Incorrect or Incomplete Suggestions

Some initial suggestions were not suitable for the final implementation, particularly approaches involving unnecessary requests to individual detail pages.

These were tested and simplified based on the actual assignment requirements and execution time.

## Verification

The final implementation was tested locally using:

```powershell
pytest -v
```

Result:

```text
20 passed
```

The scraper was also executed against both target websites:

```powershell
python main.py
```

Final results:

- Books: 1,000
- Quotes: 100
- Total scraped: 1,100
- Valid: 1,100
- Rejected: 0
- Duplicates removed: 1
- Final records: 1,099

The generated CSV, JSON summary, and log files were manually reviewed.

## Final Responsibility

AI was used only as a supporting tool. The final coding, debugging, testing, execution, and verification were performed by the developer.
