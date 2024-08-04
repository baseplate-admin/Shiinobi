import datetime

import requests

from shiinobi.parser.anime_producer import AnimeProducerParser
from shiinobi.utilities.session import session


def get_producer_res_given_mal_id(mal_id: int) -> requests.Response:
    return session.get(f"https://myanimelist.net/anime/producer/{mal_id}")


def test_first_producer_parser() -> None:
    res = get_producer_res_given_mal_id(1)
    parser = AnimeProducerParser(res.text)

    data = parser.build_dictionary()

    assert int(data["mal_id"]) == 1
    assert data["name"] == "Pierrot"
    assert data["name_japanese"] == "ぴえろ"
    assert data["established"] == datetime.datetime(1979, 5, 1, 0, 0)
