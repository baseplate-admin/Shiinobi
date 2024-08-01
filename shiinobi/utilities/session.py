from typing import Any

from requests import Session
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict
from requests.utils import DEFAULT_ACCEPT_ENCODING
from requests_cache import SQLiteCache, CacheMixin
from requests_ratelimiter import LimiterMixin, SQLiteBucket
from urllib3.util import Retry


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """
    Session class with caching and rate-limiting behavior.
        Accepts arguments for both LimiterSession and CachedSession.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.headers = self.default_headers()

    def default_headers(self) -> CaseInsensitiveDict[str | bytes]:
        """
        :rtype: requests.structures.CaseInsensitiveDict
        """
        return CaseInsensitiveDict(
            {
                "User-Agent": "CoreProject",
                "Accept-Encoding": DEFAULT_ACCEPT_ENCODING,
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
        )


RETRY_STATUSES = [403]

retry_strategy = Retry(
    total=15,
    backoff_factor=2,
    status_forcelist=RETRY_STATUSES,
)
adapter = HTTPAdapter(max_retries=retry_strategy)


session = CachedLimiterSession(
    bucket_class=SQLiteCache,
    cache_name="http_cache",
    backend=SQLiteBucket(identity="ratelimiter"),
    # https://docs.api.jikan.moe/#section/Information/Rate-Limiting
    per_minute=100,
    # per_second=1,
    per_host=True,
    # https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html
    expire_after=360,
)
session.mount("http://", adapter)
session.mount("https://", adapter)
