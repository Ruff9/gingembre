import pytest

@pytest.fixture(scope='session')
def splinter_screenshot_dir():
    return 'test_screenshots'

@pytest.fixture(scope='session')
def splinter_headless():
    return True