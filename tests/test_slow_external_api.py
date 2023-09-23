# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from http import HTTPStatus
import requests
import pytest


@pytest.mark.slow()
def test_slow_api_url_1() -> None:
    """Test that slow (2 seconds) api url is accessible."""
    response = requests.get('https://my-json-server.typicode.com/typicode/demo/posts?_delay=2000')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.slow()
def test_slow_api_url_2() -> None:
    """Test that slow (4 seconds) api url is accessible."""
    response = requests.get('https://my-json-server.typicode.com/typicode/demo/posts?_delay=4000')
    assert response.status_code == HTTPStatus.OK
