import pytest

from pytest_factoryboy import register
import factories

register(factories.ChatUserFactory)

@pytest.fixture(scope='session')
def splinter_screenshot_dir():
    return 'test_screenshots'

@pytest.fixture(scope='session')
def splinter_headless():
    return True