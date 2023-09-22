# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from pydantic import BaseModel
from http import HTTPStatus
import pytest

from django.test import Client
from django.urls import reverse_lazy

from server.apps.identity.models import User


@pytest.fixture()
def assert_create_correct_user_data():
    """Compare received new user data and data from database"""

    def factory(email: str, register_user_data: BaseModel) -> None:
        user = User.objects.get(email=email)
        assert user.id
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

        for field_name, data_value in register_user_data.model_dump().items():
            if field_name == 'date_of_birth':
                # type date -> str
                assert getattr(user, field_name).strftime('%Y-%m-%d') == data_value
                continue
            if field_name.startswith('password'):
                # skip password fields
                continue
            assert getattr(user, field_name) == data_value

    return factory


@pytest.fixture()
def assert_external_api_lead_id_create():
    """ Compare received external API lead_id and lead_id from database"""

    def factory(email: str, external_lead_id: int) -> None:
        user = User.objects.get(email=email)
        assert user.lead_id == external_lead_id

    return factory


@pytest.mark.django_db
def test_valid_create_new_user(client: Client,
                               user_data_generate: BaseModel,
                               external_api_post_mock,
                               assert_create_correct_user_data,
                               assert_external_api_lead_id_create) -> None:
    """Test create new regular user with random generate data and check external API 'lead_id' create"""
    response = client.post(reverse_lazy('identity:registration'), data=user_data_generate.model_dump())

    assert response.status_code == HTTPStatus.FOUND
    assert response.headers['Location'] == reverse_lazy('identity:login')

    assert_create_correct_user_data(user_data_generate.email, user_data_generate)
    assert_external_api_lead_id_create(user_data_generate.email, external_api_post_mock['id'])
