import pytest
from django.urls import reverse
from messenger.models import ChatUser


@pytest.mark.django_db
class TestChatUsers:
    def test_chat_user_creation(self, live_server, browser):
        browser.visit(live_server.url + reverse('home'))

        username_field = browser.find_by_css('form input[name="username"]')
        username_field.fill("Bobby")

        submit = browser.find_by_css('form input[type="submit"]')
        submit.click()

        chat_user = ChatUser.objects.latest("created_at")

        assert chat_user.username == "Bobby"
        assert browser.url == (live_server.url + reverse('index'))