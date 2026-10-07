import logging
from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class BooksScraper(BaseScraper):
    """
    Scraper for Books to Scrape.
    """

    BASE_URL = "https://books.toscrape.com/"

    def scrape(self):
        """
        Scrape all books by following pagination.
        """

        books = []
        current_url = self.BASE_URL

        while current_url:
            logger.info("Scraping books page: %s", current_url)

            response = self.fetch(current_url)

            if response is None:
                logger.error(
                    "Skipping books page because request failed: %s",
                    current_url
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            book_cards = soup.select("article.product_pod")

            logger.info(
                "Found %d books on page: %s",
                len(book_cards),
                current_url
            )

            for card in book_cards:
                try:
                    book = self._parse_book(card, current_url)
                    books.append(book)

                except Exception as exc:
                    logger.exception(
                        "Failed to parse a book on %s: %s",
                        current_url,
                        exc
                    )

            next_link = soup.select_one("li.next a")

            if next_link and next_link.get("href"):
                current_url = urljoin(
                    current_url,
                    next_link["href"]
                )
            else:
                current_url = None

        logger.info(
            "Books scraping completed. Total books: %d",
            len(books)
        )

        return books

    def _parse_book(self, card, source_url):
        """
        Parse one book card.
        """

        title_element = card.select_one("h3 a")
        price_element = card.select_one("p.price_color")
        rating_element = card.select_one("p.star-rating")

        title = (
            title_element.get("title", "").strip()
            if title_element
            else ""
        )

        price = (
            price_element.get_text(strip=True)
            if price_element
            else ""
        )

        rating = ""

        if rating_element:
            rating_classes = rating_element.get("class", [])

            rating_names = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5,
            }

            for class_name in rating_classes:
                if class_name in rating_names:
                    rating = rating_names[class_name]
                    break

        book_url = ""

        if title_element and title_element.get("href"):
            book_url = urljoin(
                source_url,
                title_element["href"]
            )

        return {
            "source": "books.toscrape.com",
            "source_url": book_url,
            "name_or_title": title,
            "category": "",
            "price": price,
            "rating": rating,
            "author": "",
            "tags": "",
            "description": "",
            "scraped_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }