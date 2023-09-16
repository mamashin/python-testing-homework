# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'


import pytest
import json
import httpretty
from http import HTTPStatus
from pydantic import BaseModel
from mimesis.locales import Locale
from mimesis import Generic, Address, Person, Gender

from django.test import Client
from django.urls import reverse_lazy

from server.apps.identity.models import User
from server.settings.components import placeholder


@pytest.fixture()
def user_data_generate() -> BaseModel:
    """Generate user random data and return BaseModel object"""
    generic = Generic(Locale.RU)
    person = Person(Locale.RU)

    class UserDataGenerate(BaseModel):
        first_name: str = person.name(gender=Gender.MALE)
        last_name: str = person.last_name(gender=Gender.MALE)
        date_of_birth: str = generic.datetime.date(start=1970, end=2000).strftime('%Y-%m-%d')
        address: str = Address(Locale.RU).city()
        job_title: str = person.title(gender=Gender.MALE)
        email: str = person.email()
        phone: str = person.telephone()
        # static password for auth user
        password1: str = 'qwerty123'
        password2: str = 'qwerty123'

    return UserDataGenerate()


@pytest.fixture()
def create_new_user(client: Client, user_data_generate: BaseModel,
                    external_api_post_mock: dict) -> User:
    """Create new regular user with random generate data"""
    client.post(reverse_lazy('identity:registration'), data=user_data_generate.model_dump())
    user = User.objects.get(email=user_data_generate.email)
    assert user.id
    return user


@pytest.fixture()
def external_api_placeholder_lead_id_response(user_data_generate: BaseModel):
    """Return external_placeholder_lead_id_response"""
    response_model_dict = user_data_generate.model_dump()
    response_model_dict['id'] = Generic().code.random.randint(1, 999)

    return response_model_dict


@pytest.fixture()
def external_api_post_mock(external_api_placeholder_lead_id_response):
    """Mock external API
    (call from  server.apps.identity.intrastructure.services.placeholder.LeadCreate)"""
    with httpretty.httprettized(verbose=True, allow_net_connect=True):
        httpretty.register_uri(
            method=httpretty.POST,
            uri=f'{placeholder.PLACEHOLDER_API_URL}users',
            body=json.dumps(external_api_placeholder_lead_id_response),
            status=HTTPStatus.CREATED
        )
        yield external_api_placeholder_lead_id_response
        # assert httpretty.has_request()
