from scrapers.books_scraper import BooksScraper


def test_books_scraper():
    scraper = BooksScraper(delay=0)

    books = scraper.scrape()

    assert books
    assert len(books) > 0

    first_book = books[0]

    assert first_book["source"] == "books.toscrape.com"
    assert first_book["name_or_title"]
    assert first_book["price"]
    assert first_book["rating"]
    assert first_book["source_url"]