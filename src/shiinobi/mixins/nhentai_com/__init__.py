from shiinobi.utilities import get_session
from shiinobi.facades import StringFacade, RegexFacade, LogFacade
from selectolax.parser import HTMLParser
import cloudscraper

__all__ = ["NhentaiComClientWithHelper"]


class NhentaiComClientWithHelper(StringFacade, RegexFacade, LogFacade):
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
        - client
        - logger
    """

    def __init__(self):
        StringFacade.__init__(self)
        RegexFacade.__init__(self)
        LogFacade.__init__(self)

        # Client
        self.client = get_session(
            per_minute=120,
            per_second=2,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )

        # Scraper for cloudflare protection
        self.scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)
