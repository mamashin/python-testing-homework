# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse_lazy


@pytest.mark.django_db
def test_identity_login_url(admin_client: Client) -> None:
    """Test that login page is accessible and redirect to dashboard for authenticated user."""
    response = admin_client.get(reverse_lazy('identity:login'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get('Location') == reverse_lazy('pictures:dashboard')


@pytest.mark.django_db
def test_identity_logout_url(admin_client: Client) -> None:
    """Test that logout page is accessible for authenticated user."""
    response = admin_client.get(reverse_lazy('identity:logout'))

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers.get('Location') == reverse_lazy('index')


@pytest.mark.django_db
def test_identity_registration_url(client: Client) -> None:
    """Test that logout page is accessible."""
    response = client.get(reverse_lazy('identity:registration'))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_identity_not_auth_update_url(client: Client) -> None:
    """Test that user update page is not accessible not authenticated user."""
    response = client.get(reverse_lazy('identity:user_update'))

    assert response.status_code != HTTPStatus.OK


@pytest.mark.django_db
def test_identity_auth_update_url(admin_client: Client) -> None:
    """Test that user update page is not accessible not authenticated user."""
    response = admin_client.get(reverse_lazy('identity:user_update'))

    assert response.status_code == HTTPStatus.OK
