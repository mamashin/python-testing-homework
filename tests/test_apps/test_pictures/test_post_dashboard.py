# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from typing import Generator, Any, List

import pytest
from django.test import Client
from django.urls import reverse_lazy
from http import HTTPStatus

from server.apps.identity.models import User


@pytest.mark.django_db
def test_post_picture_to_favorite(client: Client,
                                  create_new_user: User,
                                  generate_pictures_list: List[dict[str, str]],
                                  external_api_get_pictures_mock: Generator[List[dict[str, str]], Any, None]) -> None:
    """Test add picture to favorite list"""
    # Authorization user
    client.login(email=create_new_user.email, password='qwerty123')

    assert create_new_user.pictures.count() == 0  # New user has no favorite pictures yet

    picture_add_post_data = {'foreign_id': generate_pictures_list[0]['id'],
                             'url': generate_pictures_list[0]['url']}

    post_add_picture_response = client.post(reverse_lazy('pictures:dashboard'),
                                            data=picture_add_post_data)

    assert post_add_picture_response.status_code == HTTPStatus.FOUND
    assert post_add_picture_response.headers['Location'] == reverse_lazy('pictures:dashboard')
    assert create_new_user.pictures.count() == 1  # User now has one favorite picture
