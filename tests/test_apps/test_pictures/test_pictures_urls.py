# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from http import HTTPStatus
import pytest

from django.test import Client
from django.urls import reverse_lazy


pytestmark = pytest.mark.parametrize('url_name', ['pictures:dashboard', 'pictures:favourites'])


@pytest.mark.django_db
def test_pictures_non_auth_url(client: Client, url_name) -> None:
    """Test that pictures pages is not accessible for not authenticated user and redirect to login page."""
    response = client.get(reverse_lazy(url_name))

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get('Location').startswith(str(reverse_lazy('identity:login')))


@pytest.mark.django_db
def test_pictures_auth_url(admin_client: Client, url_name) -> None:
    """Test that pictures pages is accessible for authenticated user."""
    response = admin_client.get(reverse_lazy(url_name))

    assert response.status_code == HTTPStatus.OK
