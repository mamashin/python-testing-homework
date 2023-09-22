# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

import pytest
from typing import Final

SLOW_TIMEOUT: Final = 60  # seconds


def pytest_addoption(parser):
    parser.addoption(
        '--with-slow', action='store_true',
        default=False, help='enable slow tests (only run in CI)',
    )


def pytest_collection_modifyitems(
        session: pytest.Session,
        config: pytest.Config,
        items: list[pytest.Item],
        ) -> None:
    for item in items:
        slow_marker = item.get_closest_marker(name='slow')
        if slow_marker:
            item.add_marker(pytest.mark.timeout(SLOW_TIMEOUT))
            if not config.getoption('with_slow'):
                item.add_marker(pytest.mark.skip('slow test (add --with-slow)'))
