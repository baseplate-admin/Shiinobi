from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import signal

from shiinobi.constants.nhentai import MAX_WORKER
from shiinobi.mixins.nhentai import NhentaiClientWithHelper

__all__ = ["NHentaiNumberBuilder"]


class NHentaiNumberBuilder(NhentaiClientWithHelper):
    """The base class for nhentai number builder"""

    def __init__(self) -> None:
        super().__init__()
        self._num_pages = self.__build_page_num()
        self._interrupted = False

    def __build_page_num(self):
        res = self.client.get(
            "https://nhentai.net/api/galleries/search?query=language:english"
        )

        data = res.json()
        return data["num_pages"]

    def fetch_page(self, page):
        if self._interrupted:
            return []

        url = "https://nhentai.net/api/galleries/search?query=language:english"

        self.logger.info(f"Fetching page {page}")
        res = self.client.get(f"{url}&page={page}")

        data = res.json()
        return [item["id"] for item in data["result"]]

    def __signal_handler(self, signum, frame):
        """Handle keyboard interrupt gracefully"""
        self._interrupted = True

    def __build_ids(self):
        # Register the signal handler
        original_sigint = signal.signal(signal.SIGINT, self.__signal_handler)

        ids = []

        try:
            with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
                future_to_page = {
                    executor.submit(self.fetch_page, page): page
                    for page in range(1, self._num_pages + 1)
                }

                for future in as_completed(future_to_page):
                    if self._interrupted:
                        break

                    try:
                        page_ids = future.result()
                        if page_ids:
                            ids.extend(page_ids)
                    except Exception as e:
                        self.logger.error(
                            f"Error fetching page {future_to_page[future]}: {e}"
                        )

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")

        finally:
            # Restore the original signal handler
            signal.signal(signal.SIGINT, original_sigint)

            if self._interrupted:
                sys.exit(0)

            return ids

    def build_dictionary(self, sort=False) -> dict[int, str]:
        ids = self.__build_ids()
        dictionary = {}

        for item in ids:
            dictionary.setdefault(item, f"https://nhentai.net/g/{item}")

        return dictionary
