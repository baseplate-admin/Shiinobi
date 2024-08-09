import base64
import json
from datetime import datetime
from io import BytesIO
from typing import Literal, Optional

import typer
from typing_extensions import Annotated

from shiinobi import __version__

from shiinobi.builder.myanimelist.anime import AnimeBuilder
from shiinobi.builder.myanimelist.anime_demographics import AnimeDemographicsBuilder
from shiinobi.builder.myanimelist.anime_explicit_genres import AnimeExplicitGenreBuilder
from shiinobi.builder.myanimelist.anime_genres import AnimeGenreBuilder
from shiinobi.builder.myanimelist.anime_theme import AnimeThemeBuilder
from shiinobi.builder.myanimelist.character import CharacterBuilder
from shiinobi.builder.myanimelist.staff import StaffBuilder
from shiinobi.parser.myanimelist.anime import AnimeParser
from shiinobi.parser.myanimelist.anime_character_and_staff_list import (
    AnimeCharacterAndStaffListParser,
)
from shiinobi.builder.myanimelist.manga_all_genres import MangaAllGenreBuilder
from shiinobi.builder.myanimelist.manga_demographics import MangaDemographicsBuilder
from shiinobi.builder.myanimelist.manga_explicit_genres import MangaExplicitGenreBuilder
from shiinobi.builder.myanimelist.manga_genres import MangaGenreBuilder
from shiinobi.builder.myanimelist.manga_maganize import MangaMaganizeBuilder
from shiinobi.builder.myanimelist.manga_theme import MangaThemeBuilder

from shiinobi.builder.myanimelist.anime_all_genres import AnimeAllGenreBuilder
from shiinobi.parser.myanimelist.anime_genre import AnimeGenreParser
from shiinobi.parser.myanimelist.anime_producer import AnimeProducerParser
from shiinobi.parser.myanimelist.character import CharacterParser
from shiinobi.parser.myanimelist.staff import StaffParser
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


def get_myanimelist_session_given_key_and_id(
    key: Literal["people", "anime", "anime/genre", "character", "anime/producer"],
    mal_id: int,
) -> session:
    return session.get(f"https://myanimelist.net/{key}/{mal_id}")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


# Anime


@app.command()
def get_myanimelist_all_anime_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeAllGenreBuilder()
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_anime_demographics(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeDemographicsBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_anime_explicit_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeExplicitGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_anime_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_anime_themes(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeThemeBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_staff_information(staff_id: int):
    res = get_myanimelist_session_given_key_and_id("people", staff_id)
    builder = StaffParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_anime_information(anime_id: int):
    res = get_myanimelist_session_given_key_and_id("anime", anime_id)
    builder = AnimeParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_anime_character_and_staff_list_information(anime_id: int):
    res = get_myanimelist_session_given_key_and_id("anime", anime_id)
    builder = AnimeCharacterAndStaffListParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_anime_genre_information(genre_id: int):
    res = get_myanimelist_session_given_key_and_id("anime/genre", genre_id)
    builder = AnimeGenreParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_character_information(character_id: int):
    res = get_myanimelist_session_given_key_and_id("character", character_id)
    builder = CharacterParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_specific_producer_information(producer_id: int):
    res = get_myanimelist_session_given_key_and_id("anime/producer", producer_id)
    builder = AnimeProducerParser(res.text)
    dictionary = builder.build_dictionary()
    print_json(dictionary)


@app.command()
def get_myanimelist_staff_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = StaffBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_anime_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_character_urls(
    excluded_ids: Annotated[Optional[list[int]], typer.Option()] = [],
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = CharacterBuilder()
    dictionary = builder.build_dictionary(excluded_ids=excluded_ids, sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_demographics(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = AnimeDemographicsBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


# Manga


@app.command()
def get_myanimelist_all_manga_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaAllGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_manga_demographics(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaDemographicsBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_manga_explicit_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaExplicitGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_manga_genres(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaGenreBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_manga_maganizes(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaMaganizeBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.command()
def get_myanimelist_manga_themes(
    sort: Annotated[Optional[bool], typer.Option()] = False,
):
    builder = MangaThemeBuilder()
    dictionary = builder.build_dictionary(sort=sort)
    print_json(dictionary)


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Prints version and exit",
        ),
    ] = None,
): ...


if __name__ == "__main__":
    app()
