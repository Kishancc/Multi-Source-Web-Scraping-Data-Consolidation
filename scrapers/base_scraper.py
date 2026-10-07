import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


logger = logging.getLogger(__name__)


class BaseScraper:
    """
    Shared HTTP functionality for all website scrapers.
    """

    def __init__(self, delay=0.5, timeout=10):
        self.delay = delay
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "ScrapingAssignment/1.0 "
                "(learning project; Python Requests)"
            )
        })

        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch(self, url):
        """
        Download a webpage and return the response.

        Returns:
            requests.Response if successful
            None if the request fails
        """

        logger.info("Fetching URL: %s", url)

        try:
            response = self.session.get(
                url,
                timeout=self.timeout
            )

            response.raise_for_status()

            # Make sure characters such as £ are handled correctly.
            response.encoding = response.apparent_encoding

            logger.info(
                "Successfully fetched %s - Status: %s",
                url,
                response.status_code
            )

            time.sleep(self.delay)

            return response

        except requests.RequestException as exc:
            logger.error(
                "Failed to fetch %s: %s",
                url,
                exc
            )

            return None