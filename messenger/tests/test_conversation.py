import pytest
from django.urls import reverse
from messenger.models import ChatUser
from factories import ChatUserFactory, MessageFactory

@pytest.mark.django_db
class TestConversations:
    def test_message_list(self, live_server, browser, mocker):
        user1 = ChatUserFactory(username='Bob')
        user2 = ChatUserFactory(username='Marcellus')

        mocker.patch(
            'messenger.views.get_current_user',
            return_value=user1
        )

        message1 = MessageFactory(sender=user1, receiver=user2, body="Yo mon gars")
        message2 = MessageFactory(sender=user1, receiver=user2, body="Bien ou quoi ?")

        browser.visit(live_server.url + reverse('conversation', kwargs={'username': user2.username}))

        assert browser.is_text_present("Marcellus") is True
        assert browser.is_text_present("Yo mon gars") is True
        assert browser.is_text_present("Bien ou quoi ?") is True
