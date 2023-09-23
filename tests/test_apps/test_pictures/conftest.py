# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from typing import Generator, Any, List
import pytest
import json
import httpretty
from server.settings.components import placeholder


@pytest.fixture()
def generate_pictures_list() -> List[dict[str, str]]:
    """Generate 5 pictures list (static), looks like:
    [{'id': 1, 'url': 'https://via.placeholder.com/600/92c952'}, ... ]
    """
    pict_color_list = ['92c952', '771796', '24f355', 'd32776', 'f66b97']
    pict_str_list = [f'{{"id": {index}, "url": "https://via.placeholder.com/600/{pict}"}}'
                     for index, pict in enumerate(pict_color_list, start=1)]
    pict_dict_list = [json.loads(idx.replace("'", '"')) for idx in pict_str_list]
    return pict_dict_list


@pytest.fixture()
def external_api_get_pictures_mock(generate_pictures_list: List[dict[str, str]]) -> Generator:
    """Mock external API, return generate 5 pictures JSON list,
    call from server.apps.pictures.intrastructure.services.placeholder.PicturesFetch"""
    with httpretty.httprettized():
        httpretty.register_uri(
            method=httpretty.GET,
            uri=f'{placeholder.PLACEHOLDER_API_URL}photos?_limit=10',
            body=json.dumps(generate_pictures_list)
        )
        yield generate_pictures_list
        # assert httpretty.has_request()
