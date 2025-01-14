import re

__all__ = ["RegexHelper"]


class RegexHelper:
    # Getters
    # -------
    @staticmethod
    def get_id_from_url(url: str) -> int:
        pattern = re.compile(r"/(\d+)/")

        _match = re.search(pattern, url)
        if not _match:
            raise Exception("No match found")

        _id = _match.group(1)
        if not _id.isdigit():
            raise Exception("Id is not a digit.")

        return int(_id)

    @staticmethod
    def get_content_between_first_brackets(text: str) -> str:
        pattern = re.compile(r"\((.*?)\)")
        if content := re.search(pattern, text):
            return content.group(1)
        else:
            raise Exception("No content found")

    @staticmethod
    def get_first_integer_from_url(text: str) -> int:
        pattern = r"\/(\d+)\/"
        _matches = re.search(pattern, text)
        if not _matches:
            raise Exception("There is no match")
        _id = _matches.group(1)
        if not _id.isdigit():
            raise Exception("Id is not a digit.")

        return int(_id)

    # Checks
    # -------
    @staticmethod
    def check_if_string_contains_integer(string: str) -> bool:
        pattern = re.compile(r"\d+")
        return bool(re.search(pattern, string))

    @staticmethod
    def check_if_string_contains_bracket(string: str) -> bool:
        pattern = re.compile(r"\[\d+\]")
        return bool(re.search(pattern, string))

    # Replacements
    # ------------
    @staticmethod
    def replace_br_with_newline(text: str) -> str:
        return re.sub(r"<br\s*\/?>", "\n", text)

    @staticmethod
    def remove_anime_from_the_end_of_a_string(text: str) -> str:
        pattern = r"(.*?)\sAnime"
        return re.sub(pattern, r"\1", text)

    @staticmethod
    def remove_multiple_newline(text: str) -> str:
        return re.sub(r"\n+", "\n", text)
