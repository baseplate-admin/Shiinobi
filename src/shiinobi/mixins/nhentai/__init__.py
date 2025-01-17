from shiinobi.utilities import get_logger, get_session
from shiinobi.constants.nhentai import MAX_WORKER
from shiinobi.facades import StringFacade, RegexFacade, LogFacade

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
        super().__init__()

        # Client
        self.client = get_session(
            # https://github.com/KurtBestor/Hitomi-Downloader/blob/5dc3b7f464708dd56e91a00900b9ab0dbc084494/src/extractor/nhentai_downloader.py#L24
            per_minute=MAX_WORKER * 60,
            per_second=MAX_WORKER,
            # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
            per_host=True,
        )
