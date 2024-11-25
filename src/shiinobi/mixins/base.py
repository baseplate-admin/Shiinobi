from selectolax.parser import HTMLParser


from shiinobi.mixins.client import ClientMixin
from shiinobi.utilities.regex import RegexHelper
from shiinobi.utilities.string import StringHelper

__all__ = ["BaseClientWithHelperMixinMixin"]


class BaseClientWithHelperMixinMixin(ClientMixin):
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
    """

    def __init__(self):
        # Facades
        self.regex_helper = RegexHelper()
        self.string_helper = StringHelper()

    @staticmethod
    def get_parser(html: str) -> HTMLParser:
        return HTMLParser(html)
