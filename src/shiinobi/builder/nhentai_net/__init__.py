from shiinobi.mixins.nhentai_net import NhentaiNetClientWithHelper

__all__ = ["NHentaiNetNumberBuilder"]


class NHentaiNetNumberBuilder(NhentaiNetClientWithHelper):
    """The base class for anime genre builder"""

    def __init__(self):
        super().__init__()

        self.last_page = self.__build_last_page()

    def __build_last_page(self) -> int:
        res = self.client.get("https://nhentai.net/?page=1")
        html = res.text

        parser = self.get_parser(html)
        last_page = parser.css("a.last")
        if len(last_page) != 1:
            raise ValueError("Too many last element found")

        last_page = last_page[0]
        return self.regex_helper.get_the_first_integer_from_string(
            last_page.attributes["href"]
        )

    def __build_ids(self, anchors: list[str]) -> list[int]:
        ids = [self.regex_helper.get_first_integer_from_url(item) for item in anchors]
        self.logger.debug(
            f"Building {len(ids)} ID information for `{self.__class__.__name__}` where anchor length is {len(anchors)}"
        )
        return ids

    def __build_urls(self) -> list[str]:
        urls = set()
        for page in range(self.last_page + 1, 1, -1):
            res = self.client.get(f"https://nhentai.net/?page={page}")
            html = res.text

            parser = self.get_parser(html)
            anchors = parser.css('a[href^="/g/"][href$="/"]')

            for anchor in anchors:
                href = anchor.attributes["href"]
                url = self.add_nhentai_net_if_not_already_there(href)
                urls.add(url)

                self.logger.debug(
                    f"Got anchor information for {href} in `{self.__class__.__name__}`"
                )

        return urls

    def build_dictionary(self, sort=False) -> dict[int, str]:
        urls = self.__build_urls()
        ids = self.__build_ids(urls)

        dictionary = dict(zip(ids, urls))

        if sort:
            dictionary = dict(sorted(dictionary.items()))

        return {}
