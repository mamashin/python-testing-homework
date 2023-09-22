# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from typing import Generator, List, Any

import pytest
from django.test import Client
from django.urls import reverse_lazy
from http import HTTPStatus

from server.apps.identity.models import User


@pytest.mark.django_db
def test_get_picture_dashboard(client: Client,
                               create_new_user: User,
                               generate_pictures_list: List[dict[str, str]],
                               external_api_get_pictures_mock: Generator[List[dict[str, str]], Any, None]) -> None:
    """Test get picture dashboard with authorization user"""
    # Authorization user
    client.login(email=create_new_user.email, password='qwerty123')

    dashboard_get_response = client.get(reverse_lazy('pictures:dashboard'))
    assert dashboard_get_response.status_code == HTTPStatus.OK
    assert create_new_user.pictures.count() == 0  # New user has no favorite pictures yet
