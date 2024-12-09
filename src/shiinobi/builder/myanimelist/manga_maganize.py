from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper

__all__ = ["MangaMaganizeBuilder"]


class MangaMaganizeBuilder(MyAnimeListClientWithHelper):
    """The base class for manga magazine builder"""

    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[str] = []

    def __build_ids(self) -> list[int]:
        ids = [
            self.regex_helper.get_first_integer_from_url(item) for item in self.anchors
        ]
        self.logger.debug(
            f"Building {len(ids)} ID information for `{self.__class__.__name__}` where anchor length is {len(self.anchors)}"
        )
        return ids

    def __build_urls(self, html: str) -> list[str]:
        parser = self.get_parser(html)
        theme_parent_node = (
            parser.select("div.normal_header")
            .text_contains("Magazines")
            .matches[0]
            .next.next
        )
        theme_anchor_nodes = theme_parent_node.css('a[href*="magazine"]')

        self.anchors = [
            self.string_helper.add_myanimelist_if_not_already_there(
                anchor.attributes["href"]
            )
            for anchor in theme_anchor_nodes
            if anchor.attributes["href"]
        ]
        self.logger.debug(
            f"Building {len(self.anchors)} Anchor information for `{self.__class__.__name__}`"
        )
        return self.anchors

    def build_dictionary(self, sort=False) -> dict[int, str]:
        res = self.client.get("https://myanimelist.net/manga.php")
        html = res.text

        urls = self.__build_urls(html)
        ids = self.__build_ids()

        dictionary = dict(zip(ids, urls))

        if sort:
            dictionary = dict(sorted(dictionary.items()))

        return dictionary
