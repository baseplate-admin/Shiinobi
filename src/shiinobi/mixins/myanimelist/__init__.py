from selectolax.parser import HTMLParser

from shiinobi.utilities.regex import RegexHelper
from shiinobi.utilities.session import get_session

from shiinobi.utilities.logger import get_logger
from shiinobi.utilities.string import StringHelper

__all__ = ["MyAnimeListClientWithHelper"]


class MyAnimeListClientWithHelper:
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
        - client
    """

    def __init__(self):
        # Facades
        self.regex_helper = RegexHelper()
        self.string_helper = StringHelper()

        # Client
        self.client = get_session(
            # https://docs.api.jikan.moe/#section/Information/Rate-Limiting
            per_minute=60,
            per_second=3,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )

        # Logger
        self.logger = get_logger()

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)
