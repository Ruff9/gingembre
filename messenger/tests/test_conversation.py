import pytest
from django.urls import reverse
from messenger.models import ChatUser, Message
from factories import ChatUserFactory, ConversationFactory, MessageFactory


@pytest.mark.django_db
class TestConversations:
    def test_message_list(self, live_server, browser, mocker):
        user1 = ChatUserFactory(username='Bob')
        user2 = ChatUserFactory(username='Marcellus')

        mocker.patch(
            'messenger.views.get_current_user',
            return_value=user1
        )

        conversation = ConversationFactory(user1=user1, user2=user2)
        message1 = MessageFactory(conversation=conversation, sender=user1, content="Yo mon gars")
        message2 = MessageFactory(conversation=conversation, sender=user1, content="Bien ou quoi ?")

        browser.visit(live_server.url + reverse('index'))

        link = browser.links.find_by_partial_href(f'conversation/{conversation.id}')
        link.click()

        assert browser.is_text_present("Marcellus") is True
        assert browser.is_text_present("Yo mon gars") is True
        assert browser.is_text_present("Bien ou quoi ?") is True

    # Integration testing with sockets, setup to find 
    @pytest.mark.skip
    def test_message_creation(self, live_server, browser, mocker):
        user1 = ChatUserFactory(username='Bob')
        user2 = ChatUserFactory(username='Marcellus')
        conversation = ConversationFactory(user1=user1, user2=user2)

        mocker.patch(
            'messenger.views.get_current_user',
            return_value=user1
        )

        browser.visit(live_server.url + reverse('conversation', kwargs={'conversation_id': conversation.id}))

        message_field = browser.find_by_css('form input[id="message-input"]')
        message_field.fill("Tu fais quoi ce soir?")

        submit = browser.find_by_css('form input[type="submit"]')
        submit.click()

        message = Message.objects.latest()

        assert message.content == "Tu fais quoi ce soir?"
        assert message.sender == user1

        assert browser.is_text_present("Tu fais quoi ce soir?") is True

# TODO test with two browser and two current users to test interaction live