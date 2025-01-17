import datetime
from functools import lru_cache

from dataclasses import dataclass, asdict
from dateutil import parser

from selectolax.parser import Node
from shiinobi.decorators import return_on_error
from shiinobi.mixins.myanimelist import MyAnimeListClientWithHelper

__all__ = ["AnimeParser"]


@dataclass(frozen=True)
class AnimeDictionary:
    mal_id: int
    name: str
    name_japanese: str
    name_synonyms: list[str]
    source: str
    aired_from: datetime.datetime
    aired_to: datetime.datetime
    synopsis: str
    background: str
    rating: str
    genres: list[int]
    themes: list[int]
    studios: list[int]
    producers: list[int]
    demographics: list[int]
    recommendations: list[int]
    openings: list[int]
    endings: list[int]


class AnimeParser(MyAnimeListClientWithHelper):
    def __init__(self, html: str) -> None:
        super().__init__()
        self.parser = self.get_parser(html)

    @property
    @return_on_error("")
    def get_anime_url(self):
        if anime_url := self.parser.css_first("meta[property='og:url']").attributes[
            "content"
        ]:
            return anime_url
        else:
            raise AttributeError("`get_anime_url` element not found")

    @property
    @return_on_error("")
    def get_anime_id(self):
        if anime_id := self.regex_helper.get_id_from_url(self.get_anime_url):
            return str(anime_id)
        else:
            raise AttributeError("`get_anime_id` element not found")

    @property
    @return_on_error("")
    def get_anime_name(self):
        if anime_name := self.parser.css_first("meta[property='og:title']").attributes[
            "content"
        ]:
            return anime_name
        else:
            raise AttributeError("`get_anime_name` element not found")

    @property
    @return_on_error("")
    def get_anime_name_japanese(self):
        node = self.parser.select("span").text_contains("Japanese:").matches
        if len(node) > 1:
            raise ValueError("There are more than one node in name japanese node")

        name_japanese = self.string_helper.cleanse(node[0].next.text())
        return name_japanese

    @property
    @return_on_error([])
    def get_anime_name_synonyms(self):
        node = self.parser.select("h2").text_contains("Alternative Titles").matches[0]
        alternate_names = []

        next_node: Node = None

        while True:
            if node.next.tag == "h2":
                break
            elif node.next.tag == "div":
                if node.next:
                    next_node = node.next

            try:
                alternate_name = self.string_helper.cleanse(
                    next_node.css_first("span").next.text()
                )
                alternate_names.append(alternate_name)

                next_node.decompose(recursive=True)

            # There are no nodes
            except AttributeError:
                break

        return alternate_names

    @property
    @return_on_error("")
    def get_source(self):
        node = self.parser.select("span").text_contains("Source:").matches
        if len(node) > 1:
            raise ValueError("There are multiple source node")

        source = self.string_helper.cleanse(node[0].next.text())
        return source

    @property
    @return_on_error("")
    @lru_cache(maxsize=None)
    def __get_aired_text(self):
        # aired text contains in this format
        # '<aired_from> to <aired_to>'
        node = self.parser.select("span").text_contains("Aired:").matches
        if len(node) > 1:
            raise ValueError("There are multiple aired node")

        return self.string_helper.cleanse(node[0].next.text())

    @property
    @return_on_error("")
    def get_aired_from(self):
        aired_text = self.__get_aired_text
        splitted_text = aired_text.split("to")
        aired_from = parser.parse(self.string_helper.cleanse(splitted_text[0]))
        return aired_from.isoformat()

    @property
    @return_on_error("")
    def get_aired_to(self):
        aired_text = self.__get_aired_text
        splitted_text = aired_text.split("to")
        aired_to = parser.parse(self.string_helper.cleanse(splitted_text[1]))
        return aired_to.isoformat()

    @property
    @return_on_error("")
    def get_synopsis(self):
        node = self.parser.css_first("p[itemprop='description']")

        synopsis = self.string_helper.cleanse(node.text())
        return (
            ""
            if "No synopsis information has been added to this title." in synopsis
            else synopsis
        )

    @property
    @return_on_error("")
    def get_background(self):
        node = self.parser.select("h2").text_contains("Background").matches
        if len(node) > 1:
            raise ValueError("There are multiple Background node")

        parent_node = node[0].parent.parent
        parent_node.strip_tags(["p", "div"])

        background = self.string_helper.cleanse(parent_node.text())
        return background

    @property
    @return_on_error("")
    def get_rating(self):
        node = self.parser.select("span").text_contains("Rating:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Rating node")

        rating = self.string_helper.cleanse(node[0].next.text())
        return rating

    @property
    @return_on_error([])
    def get_genres(self):
        node = self.parser.select("span").text_contains("Genres:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Genre node")

        genre_parent_nodes = node[0].parent
        # Remove all span tags
        anchor_tags = genre_parent_nodes.css("a[href*='/anime/']")
        return sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
                if anchor.attributes["href"]
            }
        )

    @property
    @return_on_error([])
    def get_themes(self):
        node = self.parser.select("span").text_contains("Themes:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Genre node")

        theme_parent_nodes = node[0].parent
        anchor_tags = theme_parent_nodes.css("a[href*='/anime/']")
        return sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
                if anchor.attributes["href"]
            }
        )

    @property
    @return_on_error([])
    def get_studios(self):
        node = self.parser.select("span").text_contains("Studios:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Studio node")

        anchor_tags = node[0].parent.css("a[href*='/producer/']")
        return sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
                if anchor.attributes["href"]
            }
        )

    @property
    @return_on_error([])
    def get_producers(self):
        node = self.parser.select("span").text_contains("Producers:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Producer node")

        anchor_tags = node[0].parent.css("a[href*='/producer/']")
        return sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
                if anchor.attributes["href"]
            }
        )

    @property
    @return_on_error([])
    def get_demographics(self):
        node = self.parser.select("span").text_contains("Demographic:").matches
        if len(node) > 1:
            raise ValueError("There are multiple Demographic node")

        anchor_tags = node[0].parent.css("a[href*='/genre/']")
        return sorted(
            {
                self.regex_helper.get_first_integer_from_url(anchor.attributes["href"])
                for anchor in anchor_tags
                if anchor.attributes["href"]
            }
        )

    @property
    @return_on_error({})
    def get_openings(self):
        node = self.parser.select("h2").text_contains("Opening Theme").matches

        opening_table_tag = node[0].parent.next.next
        # stupid myanimelist shows popup as table
        opening_table_tag.strip_tags(["div#js-oped-popup"])
        openings: dict[int, str] = {}

        table_rows = opening_table_tag.css("tr")
        for row in table_rows:
            colon_spilitted_text = row.text().split(":")
            # There are no colons in text
            # "Hikaru nara"
            if len(colon_spilitted_text) == 1:
                openings[1] = self.string_helper.cleanse(colon_spilitted_text[0])

            # "1: Hikaru nara"
            else:
                openings[int(colon_spilitted_text[0])] = self.string_helper.cleanse(
                    colon_spilitted_text[1]
                )

        return openings

    @property
    @return_on_error({})
    def get_endings(self):
        node = self.parser.select("h2").text_contains("Ending Theme").matches

        endings_table_tag = node[0].parent.next.next
        # stupid myanimelist shows popup as table
        endings_table_tag.strip_tags(["div#js-oped-popup"])
        endings: dict[int, str] = {}

        table_rows = endings_table_tag.css("tr")
        for row in table_rows:
            colon_spilitted_text = row.text().split(":")
            # There are no colons in text
            # "Hikaru nara"
            if len(colon_spilitted_text) == 1:
                endings[1] = self.string_helper.cleanse(colon_spilitted_text[0])

            # "1: Hikaru nara"
            else:
                endings[int(colon_spilitted_text[0])] = self.string_helper.cleanse(
                    colon_spilitted_text[1]
                )

        return endings

    def build_dictionary(self):
        dictionary = AnimeDictionary(
            self.get_anime_id,
            self.get_anime_name,
            self.get_anime_name_japanese,
            self.get_anime_name_synonyms,
            self.get_source,
            self.get_aired_from,
            self.get_aired_to,
            self.get_synopsis,
            self.get_background,
            self.get_rating,
            self.get_genres,
            self.get_themes,
            self.get_studios,
            self.get_producers,
            self.get_demographics,
            [],  # self.recommendations
            self.get_openings,
            self.get_endings,
        )
        return asdict(dictionary)
