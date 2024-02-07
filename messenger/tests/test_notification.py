import pytest
from django.urls import reverse
from factories import ChatUserFactory, ConversationFactory, MessageFactory, NotificationFactory


@pytest.fixture
def setup(mocker):
    user1, user2, user3 = ChatUserFactory.create_batch(3)

    mocker.patch(
        'messenger.views.get_current_user',
        return_value=user1
    )

    conversation1 = ConversationFactory(user1=user1, user2=user2)

    yield user1, user2, user3, conversation1

    user1.delete()
    user2.delete()
    user3.delete()


@pytest.mark.django_db
class TestNotifications:
    def test_notification_on_user_list(self, live_server, browser, setup):
        user1, user2, user3, conversation1 = setup

        message1 = MessageFactory(conversation=conversation1, sender=user2, content="Salut")
        NotificationFactory(message=message1, recipient=user1)

        conversation2 = ConversationFactory(user1=user1, user2=user3)
        message2 = MessageFactory(conversation=conversation2, sender=user3, content="Yo")
        message3 = MessageFactory(conversation=conversation2, sender=user3, content="T'es là?")
        NotificationFactory(message=message2, recipient=user1)
        NotificationFactory(message=message3, recipient=user1)

        browser.visit(live_server.url + reverse('index'))

        notif1_xpath = self.index_notif_container_xpath(conversation1, '1')
        assert browser.is_element_present_by_xpath(notif1_xpath) is True

        notif2_xpath = self.index_notif_container_xpath(conversation2, '2')
        assert browser.is_element_present_by_xpath(notif2_xpath) is True


    def index_notif_container_xpath(self, conversation, content):
        return (
            f"""//a[contains(@href, 'conversation/{conversation.id}')]/div[@class='user-link-name']
            /div[@class='notification-container']/p[contains(text(),'{content}')]"""
        )


    def test_notifications_on_conversation_page(self, live_server, browser, setup):
        user1, user2, user3, conversation1 = setup

        browser.visit(live_server.url + reverse('conversation', kwargs={'conversation_id': conversation1.id}))

        xpath = f"//a[contains(@href, 'index')]/div[@class='notification-container']/p[contains(text(),'2')]"
        assert browser.is_element_present_by_xpath(xpath) is False

        conversation2 = ConversationFactory(user1=user1, user2=user3)
        message2 = MessageFactory(conversation=conversation2, sender=user3, content="Yo")
        message3 = MessageFactory(conversation=conversation2, sender=user3, content="T'es là?")
        NotificationFactory(message=message2, recipient=user1)
        NotificationFactory(message=message3, recipient=user1)

        assert browser.is_element_present_by_xpath(xpath) is True
