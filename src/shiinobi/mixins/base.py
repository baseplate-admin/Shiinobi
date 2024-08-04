from selectolax.parser import HTMLParser

from shiinobi.utilities.regex import RegexHelper
from shiinobi.utilities.session import session
from shiinobi.utilities.string import StringHelper

__all__ = ["BaseClientWithHelper"]


class BaseClientWithHelper:
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
        - session
    """

    def __init__(self):
        # Facades
        self.regex_helper = RegexHelper()
        self.string_helper = StringHelper()

        # Client
        self.client = session

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)
