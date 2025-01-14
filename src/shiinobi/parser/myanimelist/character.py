# Code Owners : `horidesu`, `baseplate-admin`
# Licensed Under : AGPL-v3

from io import BytesIO
from dataclasses import dataclass, asdict
from shiinobi.decorators import return_on_error
from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper

__all__ = ["CharacterParser"]


@dataclass(frozen=True)
class CharacterImageDictionary:
    image: BytesIO
    mimetype: str


@dataclass(frozen=True)
class CharacterDictionary:
    mal_id: str
    name: str
    name_kanji: str
    character_image: CharacterImageDictionary
    about: str


class CharacterParser(MyAnimeListClientWithHelper):
    def __init__(self, html: str):
        super().__init__()

        self.parser = self.get_parser(html)

    @property
    @return_on_error("")
    def get_character_url(self):
        if character_url := self.parser.css_first("meta[property='og:url']").attributes[
            "content"
        ]:
            return character_url
        else:
            raise AttributeError("`get_character_url` element not found")

    @property
    @return_on_error("")
    def get_character_id(self):
        if character_id := self.regex_helper.get_id_from_url(self.get_character_url):
            return character_id
        else:
            raise AttributeError("`get_character_id` element not found")

    @property
    @return_on_error("")
    def get_character_name(self):
        return self.parser.css_first("meta[property='og:title']").attributes["content"]

    @property
    @return_on_error("")
    def get_character_name_kanji(self):
        return self.regex_helper.get_content_between_first_brackets(
            self.parser.css_first("h2.normal_header span small").text()
        )

    @property
    @return_on_error("")
    def get_about(self):
        html = self.parser.css_first("#content table tbody tr > td:nth-of-type(2)")
        tags = ["div", "br", "table", "h2", "script"]
        html.strip_tags(tags)

        sentences = html.text().split("\n")
        text = "\n".join(sentences).strip()
        cleaned_text = self.regex_helper.remove_multiple_newline(text)
        return cleaned_text

    @property
    @return_on_error("")
    def get_character_image(self):
        url = self.parser.css_first("meta[property='og:image']").attributes["content"]
        if url:
            res = self.client.get(url)
            return CharacterImageDictionary(BytesIO(res.content), url.split(".")[-1])

    def build_dictionary(self):
        dictionary = CharacterDictionary(
            self.get_character_id,
            self.get_character_name,
            self.get_character_name_kanji,
            self.get_character_image,
            self.get_about,
        )
        return asdict(dictionary)
