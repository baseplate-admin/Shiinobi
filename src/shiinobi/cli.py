import base64
import json
from datetime import datetime
from io import BytesIO
from typing import Literal, Optional

import typer
from typing_extensions import Annotated

from shiinobi import __version__

from shiinobi.builder.anime import AnimeBuilder
from shiinobi.builder.anime_demographics import AnimeDemographicsBuilder
from shiinobi.builder.anime_explicit_genres import AnimeExplicitGenreBuilder
from shiinobi.builder.anime_genres import AnimeGenreBuilder
from shiinobi.builder.anime_theme import AnimeThemeBuilder
from shiinobi.builder.character import CharacterBuilder
from shiinobi.builder.staff import StaffBuilder
from shiinobi.parser.anime import AnimeParser
from shiinobi.parser.anime_character_and_staff_list import (
    AnimeCharacterAndStaffListParser,
)
from shiinobi.parser.anime_genre import AnimeGenreParser
from shiinobi.parser.anime_producer import AnimeProducerParser
from shiinobi.parser.character import CharacterParser
from shiinobi.parser.staff import StaffParser
from shiinobi.utilities.session import session

app = typer.Typer()


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, BytesIO):
        return base64.b64encode(obj.getvalue()).decode("utf-8")

    return str(obj)


def print_json(_dict: dict[any, any]):
    typer.echo(json.dumps(_dict, default=custom_serializer))


def get_session_given_key_and_id(
    key: Literal["people", "anime", "anime/genre", "character", "anime/producer"],
    mal_id: int,
) -> session:
    return session.get(f"https://myanimelist.net/{key}/{mal_id}")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Print version an exit",
        ),
    ] = None,
): ...


@app.command()
def get_demographics(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeDemographicsBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_anime_explicit_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeExplicitGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_anime_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_anime_themes(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeThemeBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_specific_staff_information(staff_id: int):
    res = get_session_given_key_and_id("people", staff_id)
    builder = StaffParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_anime_information(anime_id: int):
    res = get_session_given_key_and_id("anime", anime_id)
    builder = AnimeParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_anime_character_and_staff_list_information(anime_id: int):
    res = get_session_given_key_and_id("anime", anime_id)
    builder = AnimeCharacterAndStaffListParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_anime_genre_information(genre_id: int):
    res = get_session_given_key_and_id("anime/genre", genre_id)
    builder = AnimeGenreParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_character_information(character_id: int):
    res = get_session_given_key_and_id("character", character_id)
    builder = CharacterParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_specific_producer_information(producer_id: int):
    res = get_session_given_key_and_id("anime/producer", producer_id)
    builder = AnimeProducerParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_staff_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = StaffBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


@app.command()
def get_anime_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


@app.command()
def get_character_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = CharacterBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


if __name__ == "__main__":
    app()
