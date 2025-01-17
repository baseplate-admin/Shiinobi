import re
import xml.etree.ElementTree as ET
from typing import Set

from shiinobi.mixins.nhentai_com import NhentaiComClientWithHelper

__all__ = ["NhentaiComComicBuilder"]


class NhentaiComComicBuilder(NhentaiComClientWithHelper):
    """The base class for anime builder"""

    def __build_urls_to_visit(self) -> Set[int]:
        url = "https://nhentai.com/en/sitemap.xml"
        res = self.client.get(url)
        tree = ET.fromstring(res.content)

        pattern = re.compile(r"https://nhentai\.com/en/sitemap/comics/\d+\.xml")

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

        for url in urls_to_visit:
            res = self.client.get(url)
            tree = ET.fromstring(res.content)

            for entry in tree:
                for element in entry:
                    if "loc" in element.tag:
                        content = element.text
                        dictionary[self.regex_helper.get_id_from_url(content)] = content

        if sort:
            dictionary = dict(sorted(dictionary.items()))

        return dictionary
