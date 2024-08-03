import typer
import json
from io import BytesIO
import base64

from typing import Literal, Optional
from typing_extensions import Annotated

from datetime import datetime
from shiinobi.utilities.session import session
from shiinobi.builder.staff import StaffBuilder
from shiinobi.parser.staff import StaffParser
from shiinobi.builder.anime_theme import AnimeThemeBuilder

app = typer.Typer()


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, BytesIO):
        return base64.b64encode(obj.getvalue()).decode("utf-8")

    return str(obj)


def print_json(_dict: dict[any, any]):
    print(json.dumps(_dict, default=custom_serializer))


def get_url_given_key_and_id(key: Literal["people"], mal_id: int) -> session:
    return session.get(f"https://myanimelist.net/people/{mal_id}")


@app.command()
def get_anime_themes():
    builder = AnimeThemeBuilder()
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_staff_information(staff_id: int):
    url = get_url_given_key_and_id("people", staff_id)
    print_json(StaffParser(url.text).build_dictionary())


@app.command()
def get_staff_dict(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = StaffBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


if __name__ == "__main__":
    app()
