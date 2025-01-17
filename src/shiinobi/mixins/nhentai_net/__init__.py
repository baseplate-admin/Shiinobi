from shiinobi.utilities import get_session
from shiinobi.facades import StringFacade, RegexFacade, LogFacade
from selectolax.parser import HTMLParser

__all__ = ["NhentaiClientWithHelper"]


class NhentaiClientWithHelper(StringFacade, RegexFacade, LogFacade):
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
            # https://github.com/KurtBestor/Hitomi-Downloader/blob/5dc3b7f464708dd56e91a00900b9ab0dbc084494/src/extractor/nhentai_downloader.py#L24
            per_minute=120,
            per_second=2,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)

    @staticmethod
    def add_nhentai_if_not_already_there(url: str) -> str:
        if "nhentai.net" not in url:
            return "https://nhentai.net" + url
        else:
            return url
