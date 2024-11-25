from shiinobi.mixins.client import ClientMixin


__all__ = ["NHentaiNumberBuilder"]


class NHentaiNumberBuilder(ClientMixin):
    """The base class for nhentai number builder"""

    def __init__(self) -> None:
        super().__init__()
        self._num_pages = self.__build_page_num()

    def __build_page_num(self):
        res = self.client.get(
            "https://nhentai.net/api/galleries/search?query=language:english"
        )

        data = res.json()
        return data["num_pages"]

    def __build_ids(self):
        url = "https://nhentai.net/api/galleries/search?query=language:english"
        ids = []

        for page in range(1, self._num_pages + 1):
            res = self.client.get(f"{url}&page={page}")
            data = res.json()
            result = data["result"]
            for item in result:
                ids.append(item["id"])

        return ids

    def build_dictionary(self, sort=False) -> dict[int, str]:
        ids = self.__build_ids()
        dictionary = {}

        for item in ids:
            dictionary.setdefault(item, f"https://nhentai.net/g/{id}")
        return dictionary
