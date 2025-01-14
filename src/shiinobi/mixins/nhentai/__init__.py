from shiinobi.utilities.regex import RegexHelper
from shiinobi.utilities.session import get_session

from shiinobi.utilities.logger import get_logger
from shiinobi.utilities.string import StringHelper

__all__ = ["NhentaiClientWithHelper"]


class NhentaiClientWithHelper:
    """
    Base mixin that includes:
        - RegexHelper
        - StringHelper
        - client
        - logger
    """

    def __init__(self):
        # Facades
        self.regex_helper = RegexHelper()
        self.string_helper = StringHelper()

        # Client
        self.client = get_session(
            # https://docs.api.jikan.moe/#section/Information/Rate-Limiting
            per_minute=60,
            per_second=2,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )

        # Logger
        self.logger = get_logger()
