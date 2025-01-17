import re
import requests
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

        pattern = re.compile(r"https://nhentai\.com/en/sitemap/comics/d+\.xml")
        urls = set()

        urls = [
            element.text
            for sitemap in tree
            for element in sitemap
            if "loc" in element.tag and pattern.search(element.text)
        ]
        self.logger.debug(
            f"Building {len(urls)} URL information for `{self.__class__.__name__}`"
        )
        return set(urls)

    def build_dictionary(
        self, excluded_ids: list[int] | None = None, sort: bool = False
    ) -> dict[int, str]:
        dictionary = {}
        urls_to_visit = self.__build_urls_to_visit()
        print(urls_to_visit)
        if sort:
            dictionary = dict(sorted(dictionary.items()))

        return dictionary
