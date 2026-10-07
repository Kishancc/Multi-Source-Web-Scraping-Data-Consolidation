from scrapers.quotes_scraper import QuotesScraper


def test_quotes_scraper():
    scraper = QuotesScraper(delay=0)

    quotes = scraper.scrape()

    assert quotes
    assert len(quotes) > 0

    first_quote = quotes[0]

    assert first_quote["source"] == "quotes.toscrape.com"
    assert first_quote["name_or_title"]
    assert first_quote["author"]
    assert first_quote["source_url"]