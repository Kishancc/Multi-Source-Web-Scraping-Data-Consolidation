from scrapers.base_scraper import BaseScraper


def test_fetch_books_website():
    scraper = BaseScraper()

    response = scraper.fetch("https://books.toscrape.com/")

    assert response is not None
    assert response.status_code == 200
    assert "<html" in response.text.lower()