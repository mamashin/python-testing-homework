# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

import re
from http import HTTPStatus
from typing import Dict, Generator

import httpretty
import json
import pytest

from django.test import Client
from django.urls import reverse_lazy
from django.forms.models import model_to_dict

from server.apps.identity.models import User
from server.settings.components import placeholder


@pytest.fixture()
def external_api_patch_mock(external_api_placeholder_lead_id_response):
    """Mock external API
    (call from  server.apps.identity.intrastructure.services.placeholder.LeadUpdate)"""
    with httpretty.httprettized(verbose=True, allow_net_connect=True):
        httpretty.register_uri(
            method=httpretty.PATCH,
            uri=re.compile(f'{placeholder.PLACEHOLDER_API_URL}users/.*'),
            body=json.dumps(external_api_placeholder_lead_id_response),
            status=HTTPStatus.OK
        )
        yield external_api_placeholder_lead_id_response
        # assert httpretty.has_request()


@pytest.mark.django_db
def test_update_exist_user_data_field(client: Client,
                                      create_new_user: User,
                                      external_api_patch_mock: Generator) -> None:
    """Test update exist user data field"""
    create_new_user.address = 'Amsterdam'  # change address
    create_new_user.date_of_birth = create_new_user.date_of_birth.strftime('%Y-%m-%d')  # type date -> string
    select_fields: dict = model_to_dict(create_new_user, fields=User.REQUIRED_FIELDS)  # stay only required fields

    # Authorization existing user
    client.login(email=create_new_user.email, password='qwerty123')

    resp = client.post(reverse_lazy('identity:user_update'), data=select_fields)

    assert resp.status_code == HTTPStatus.FOUND
    user = User.objects.get(email=create_new_user.email)
    # Check update user data field
    assert user.address == 'Amsterdam'
