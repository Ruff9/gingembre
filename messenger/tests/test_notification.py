import pytest
from django.urls import reverse
from factories import ChatUserFactory, ConversationFactory, MessageFactory, NotificationFactory

# @pytest.mark.focus
@pytest.mark.django_db
class TestNotifications:
    def test_notification_on_message_list(self, live_server, browser, mocker):
        user1 = ChatUserFactory(username='Marco')
        user2 = ChatUserFactory(username='Clara')
        user3 = ChatUserFactory(username='Amir')

        mocker.patch(
            'messenger.views.get_current_user',
            return_value=user1
        )

        conversation1 = ConversationFactory(user1=user1, user2=user2)
        message1 = MessageFactory(conversation=conversation1, sender=user2, content="Salut")
        NotificationFactory(message=message1)

        conversation2 = ConversationFactory(user1=user1, user2=user3)
        message2 = MessageFactory(conversation=conversation2, sender=user3, content="Yo")
        message3 = MessageFactory(conversation=conversation2, sender=user3, content="T'es là?")
        NotificationFactory(message=message2)
        NotificationFactory(message=message3)

        browser.visit(live_server.url + reverse('index'))

        notif1_xpath = self.notif_container_xpath(conversation1, '1')
        assert browser.is_element_present_by_xpath(notif1_xpath) is True

        notif2_xpath = self.notif_container_xpath(conversation2, '2')
        assert browser.is_element_present_by_xpath(notif2_xpath) is True

        browser.links.find_by_partial_href(f'conversation/{conversation2.id}').click()

        assert browser.is_text_present("Yo") is True

        browser.links.find_by_partial_href('index').click()

        assert browser.is_element_present_by_xpath(notif2_xpath) is False


    def notif_container_xpath(self, conversation, content):
        xpath_str = f"//a[contains(@href, 'conversation/{conversation.id}')]/div[@class='user-link-name']/div[@class='notification-container']/p[contains(text(),'{content}')]"

        return xpath_str
