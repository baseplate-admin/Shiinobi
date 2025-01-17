from selectolax.parser import HTMLParser

from shiinobi.utilities import get_session
from shiinobi.facades import StringFacade, RegexFacade, LogFacade

__all__ = ["MyAnimeListClientWithHelper"]


class MyAnimeListClientWithHelper(StringFacade, RegexFacade, LogFacade):
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
        - client
        - logger
    """

    def __init__(self):
        super().__init__()

        # Client
        self.client = get_session(
            # https://docs.api.jikan.moe/#section/Information/Rate-Limiting
            per_minute=60,
            per_second=3,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)
