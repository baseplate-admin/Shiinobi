from shiinobi.mixins.base import BaseClientWithHelper

import xml.etree.ElementTree as ET
from typing import Set

import re


class AnimeBuilder(BaseClientWithHelper):
    def __init__(self) -> None:
        super().__init__()
        # Urls
        self.urls_to_visit = self.__build_urls_to_visit()

    def __build_urls_to_visit(self) -> Set[int]:
        url = "https://myanimelist.net/sitemap/index.xml"
        res = self.client.get(url)
        tree = ET.fromstring(res.content)

        pattern = re.compile(r"https://myanimelist\.net/sitemap/anime-\d+\.xml")

        urls = [
            element.text
            for sitemap in tree
            for element in sitemap
            if "loc" in element.tag and pattern.search(element.text)
        ]

        return set(urls)

    def build_dictionary(
        self, excluded_ids: list[int] | None = None, sort: bool = False
    ) -> dict[int, str]:
        dictionary = {}

        for url in self.urls_to_visit:
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
