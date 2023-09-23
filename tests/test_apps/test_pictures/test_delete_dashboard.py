# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from typing import Generator, Any, List

import pytest
from django.test import Client
from django.urls import reverse_lazy
from http import HTTPStatus

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db
def test_delete_picture_from_favorite(
    client: Client,
    create_new_user: User,
    generate_pictures_list: List[dict[str, str]],
    external_api_get_pictures_mock: Generator[List[dict[str, str]], Any, None]
) -> None:
    """Test delete picture from favorite list"""

    # Authorization user and add picture to favorite list
    client.login(email=create_new_user.email, password='qwerty123')
    picture_add_post_data = {'foreign_id': generate_pictures_list[0]['id'],
                             'url': generate_pictures_list[0]['url']}
    add_response = client.post(reverse_lazy('pictures:dashboard'), data=picture_add_post_data)
    assert add_response.status_code == HTTPStatus.FOUND
    assert create_new_user.pictures.count() == 1  # User now has one favorite picture

    # Try to delete no exist picture
    picture_delete_post_data = {'id': "0"}
    delete_response = client.post(reverse_lazy('pictures:favourites'), data=picture_delete_post_data)
    assert delete_response.status_code == HTTPStatus.BAD_REQUEST
    assert create_new_user.pictures.count() == 1  # User now has one favorite picture

    # Delete exist picture
    picture_delete_post_data['id'] = FavouritePicture.objects.last().id
    delete_response = client.post(reverse_lazy('pictures:favourites'), data=picture_delete_post_data)
    assert delete_response.status_code == HTTPStatus.FOUND
    assert create_new_user.pictures.count() == 0  # User now has no favorite pictures
