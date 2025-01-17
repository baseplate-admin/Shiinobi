import re
import xml.etree.ElementTree as ET
from typing import Set

from shiinobi.mixins.nhentai_com import NhentaiComClientWithHelper

__all__ = ["NhentaiComComicBuilder"]


class NhentaiComComicBuilder(NhentaiComClientWithHelper):
    """The base class for anime builder"""

    def __build_urls_to_visit(self) -> Set[int]:
        url = "https://nhentai.com/en/sitemap.xml"
        res = self.scraper.get(
            url,
            allow_redirects=True,
        )
        tree = ET.fromstring(res.content)

        pattern = re.compile(r"https?://nhentai\.com/en/sitemap/comics/\d+\.xml")
        urls = set()

        for sitemap in tree:
            for element in sitemap:
                if "loc" in element.tag and pattern.search(element.text):
                    url = element.text
                    urls.add(url)

        self.logger.debug(
            f"Building {len(urls)} URL information for `{self.__class__.__name__}`"
        )
        return urls

    def build_dictionary(
        self, excluded_ids: list[int] | None = None, sort: bool = False
    ) -> set[str]:
        dictionary = set()
        urls_to_visit = self.__build_urls_to_visit()

        for url in urls_to_visit:
            res = self.scraper.get(url)
            tree = ET.fromstring(res.content)

            for entry in tree:
                for element in entry:
                    if "loc" in element.tag:
                        url = element.text
                        dictionary.add(url)
                        self.logger.info(
                            f"Got url for {url} from `{self.__class__.__name__}`"
                        )

        return dictionary
