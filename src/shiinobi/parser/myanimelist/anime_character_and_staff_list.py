from dataclasses import dataclass, asdict
from shiinobi.decorators import return_on_error
from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper

__all__ = ["AnimeCharacterAndStaffListParser"]


@dataclass(frozen=True)
class AnimeCharacterAndStaffListDictionary:
    characters: list[int]
    staffs: list[int]


class AnimeCharacterAndStaffListParser(MyAnimeListClientWithHelper):
    def __init__(self, html: str) -> None:
        super().__init__()
        self.parser = self.get_parser(html)

    @return_on_error([])
    def get_characters(self):
        anchor_tags = self.parser.css("a[href*='/character/']")
        characters = sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
            }
        )
        self.logger.debug(
            f"Parsed `character` information from `{self.__class__.__name__}`"
        )

        return list(characters)

    @return_on_error([])
    def get_staffs(self):
        anchor_tags = self.parser.css("a[href*='/people/']")
        staffs = sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
            }
        )
        self.logger.debug(
            f"Parsed `staff` information from `{self.__class__.__name__}`"
        )

        return list(staffs)

    def build_dictionary(self) -> dict[str, list[int]]:
        dictionary = AnimeCharacterAndStaffListDictionary(
            self.get_characters(),
            self.get_staffs(),
        )
        return asdict(dictionary)
