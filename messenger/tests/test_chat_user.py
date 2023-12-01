import pytest
from django.urls import reverse
from messenger.models import ChatUser

from factories import ChatUserFactory

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

    @pytest.mark.focus
    def test_chat_user_index(self, live_server, browser, mocker):
        user1 = ChatUserFactory(username='Micheline')
        user2 = ChatUserFactory(username='Jean-Louis')
        user3 = ChatUserFactory(username='Patrick')

        mocker.patch(
            'messenger.views.get_current_user',
            return_value=user1
        )

        browser.visit(live_server.url + reverse('index'))

        link_list = browser.links.find_by_partial_href('get_conversation')

        assert len(link_list) == 2

        # cliquer sur le lien d'une convsersation et vérfier que l'url est la bonne 
