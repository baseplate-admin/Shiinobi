from datetime import timedelta

RETRY_STATUSES = [403, 429, 400]
TOTAL_RETRIES = 15
BACKOFF_FACTOR = 2
EXPIRE_AFTER = int(timedelta(hours=1).total_seconds())
