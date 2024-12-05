from dataclasses import dataclass, asdict
from typing import TypedDict

from shiinobi.decorators.return_error_decorator import return_on_error
from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper

__all__ = ["AnimeGenreParser"]


@dataclass(frozen=True)
class GenreDictionary(TypedDict):
    mal_id: int
    name: str
    description: str
    type: str


class AnimeGenreParser(MyAnimeListClientWithHelper):
    def __init__(self, html: str):
        super().__init__()

        self.parser = self.get_parser(html)

    @property
    @return_on_error("")
    def get_url(self) -> str:
        self.logger.debug(f"Parsed `url` information for `{self.__class__.__name__}`")
        return self.parser.css_first('meta[property="og:url"]').attributes["content"]

    @property
    @return_on_error("")
    def get_mal_id(self) -> int:
        self.logger.debug(
            f"Parsed `mal_id` information for `{self.__class__.__name__}`"
        )
        return self.regex_helper.get_id_from_url(self.get_url)

    @property
    @return_on_error("")
    def get_name(self) -> str:
        html = self.parser.css_first("span.di-ib.mt4")

        # Remove span nodes
        html.strip_tags(["span.fw-n"])
        actual_text = self.regex_helper.remove_anime_from_the_end_of_a_string(
            html.text()
        )
        self.logger.debug(f"Parsed `name` information for `{self.__class__.__name__}`")
        return self.string_helper.cleanse(actual_text)

    @property
    @return_on_error("")
    def get_description(self) -> str:
        text = self.parser.css_first("p.genre-description").text()
        cleaned_text = self.regex_helper.replace_br_with_newline(
            self.regex_helper.remove_multiple_newline(text)
        )
        self.logger.debug(
            f"Parsed `description` information for `{self.__class__.__name__}`"
        )

        return cleaned_text

    @property
    @return_on_error("")
    def get_type(self) -> str:
        text = self.parser.css("div.di-ib")
        # The second node actually shows the item
        actual_node = text[1]
        self.logger.debug(f"Parsed `type` information for `{self.__class__.__name__}`")

        return self.string_helper.cleanse(actual_node.text())

    def build_dictionary(self) -> dict[str, int | str]:
        dictionary = GenreDictionary(
            self.get_mal_id,
            self.get_name,
            self.get_description,
            self.get_type,
        )
        return asdict(dictionary)
