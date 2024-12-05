from typing import Any, cast

from requests import Session
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict
from requests.utils import DEFAULT_ACCEPT_ENCODING
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, SQLiteBucket
from urllib3.util import Retry

__all__ = ["get_session"]

RETRY_STATUSES = [403, 429]

retry_strategy = Retry(
    total=15,
    backoff_factor=2,
    status_forcelist=RETRY_STATUSES,
)
adapter = HTTPAdapter(max_retries=retry_strategy)


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


def get_session(per_minute=0.0, per_second=0.0, per_host=False):
    session = CachedLimiterSession(
        bucket_class=SQLiteBucket,
        cache_name="http_cache",
        backend=SQLiteCache(),
        per_minute=per_minute,
        per_second=per_second,
        per_host=per_host,
        expire_after=360,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session = cast(Session, session)

    return session
