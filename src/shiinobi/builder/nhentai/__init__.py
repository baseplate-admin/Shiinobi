from shiinobi.mixins.client import ClientMixin


__all__ = ["NHentaiNumberBuilder"]


class NHentaiNumberBuilder(ClientMixin):
    """The base class for nhentai number builder"""

    def __init__(self) -> None:
        pass

    def build_dictionary(self, sort=False) -> dict[int, str]:
        res = self.client.get(
            "https://nhentai.net/api/galleries/search?query=language:english"
        )

        no_of_pages = res.json()
        return
