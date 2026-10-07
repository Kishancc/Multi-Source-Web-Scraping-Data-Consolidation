import logging
from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


logger = logging.getLogger(__name__)


class QuotesScraper(BaseScraper):
    """
    Scraper for Quotes to Scrape.
    """

    BASE_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        """
        Scrape all quotes by following pagination.

        Returns:
            list[dict]: Scraped quote records.
        """

        quotes = []
        current_url = self.BASE_URL

        while current_url:
            logger.info("Scraping quotes page: %s", current_url)

            response = self.fetch(current_url)

            if response is None:
                logger.error(
                    "Skipping quotes page because request failed: %s",
                    current_url
                )
                break

            soup = BeautifulSoup(response.text, "lxml")

            quote_cards = soup.select("div.quote")

            logger.info(
                "Found %d quotes on page: %s",
                len(quote_cards),
                current_url
            )

            for card in quote_cards:
                try:
                    quote = self._parse_quote(card, current_url)
                    quotes.append(quote)

                except Exception as exc:
                    logger.exception(
                        "Failed to parse quote on %s: %s",
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
            "Quotes scraping completed. Total quotes: %d",
            len(quotes)
        )

        return quotes

    def _parse_quote(self, card, source_url):
        """
        Parse one quote card.
        """

        text_element = card.select_one("span.text")
        author_element = card.select_one("small.author")

        text = (
            text_element.get_text(strip=True)
            if text_element
            else ""
        )

        author = (
            author_element.get_text(strip=True)
            if author_element
            else ""
        )

        tag_elements = card.select("a.tag")

        tags = [
            tag.get_text(strip=True)
            for tag in tag_elements
        ]

        

        return {
            "source": "quotes.toscrape.com",
            "source_url": source_url,
            "name_or_title": text,
            "category": "",
            "price": "",
            "rating": "",
            "author": author,
            "tags": ", ".join(tags),
            "description": "",
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }