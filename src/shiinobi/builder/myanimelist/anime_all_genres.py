from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper


class AnimeAllGenreBuilder(MyAnimeListClientWithHelper):
    """The base class for anime genre builder"""

    def __build_ids(self, anchors: list[str]) -> list[int]:
        ids = [self.regex_helper.get_first_integer_from_url(item) for item in anchors]
        self.logger.debug(
            f"Building {len(ids)} ID information for `{self.__class__.__name__}` where anchor length is {len(anchors)}"
        )
        return ids

    def __build_urls(self, html: str) -> list[str]:
        parser = self.get_parser(html)
        theme_anchor_nodes = parser.css('a[href*="genre"]')

        anchors = [
            self.add_myanimelist_if_not_already_there(anchor.attributes["href"])
            for anchor in theme_anchor_nodes
            if anchor.attributes["href"]
        ]
        self.logger.debug(
            f"Building {len(anchors)} Anchor information for `{self.__class__.__name__}`"
        )
        return anchors

    def build_dictionary(self, sort=False) -> dict[int, str]:
        res = self.client.get("https://myanimelist.net/anime.php")
        html = res.text

        urls = self.__build_urls(html)
        ids = self.__build_ids(urls)

        dictionary = dict(zip(ids, urls))

        if sort:
            dictionary = dict(sorted(dictionary.items()))

        return dictionary
