import pytest

from pytest_factoryboy import register
import factories

register(factories.ChatUserFactory)
register(factories.ConversationFactory)
register(factories.MessageFactory)
register(factories.AsyncChatUserFactory)
register(factories.AsyncConversationFactory)

@pytest.fixture(scope='session')
def splinter_screenshot_dir():
    return 'test_screenshots'

@pytest.fixture(scope='session')
def splinter_headless():
    return True
