import pytest

from messenger.models import Notification
from messenger.notification_manager import NotificationManager
from factories import ChatUserFactory, ConversationFactory, MessageFactory, NotificationFactory


@pytest.fixture
def user1():
    return ChatUserFactory()


@pytest.fixture
def user2():
    return ChatUserFactory()


@pytest.fixture
def conversation(user1, user2):
    return ConversationFactory(user1=user1, user2=user2)


@pytest.fixture
def message1(conversation, user2):
    return MessageFactory(conversation=conversation, sender=user2)


@pytest.fixture
def message2(conversation, user1):
    return MessageFactory(conversation=conversation, sender=user1)


@pytest.mark.django_db
class TestNotificationManager:
    def test_create(self, user1):
        message = MessageFactory()

        NotificationManager.create(message, user1)

        notification = Notification.objects.latest()

        assert notification.recipient_id == user1.id
        assert notification.message_id == message.id


    def test_mark_as_read(self, user1, user2, conversation, message1, message2):
        notif1 = NotificationFactory(message=message1, recipient=user1, read=False)
        notif2 = NotificationFactory(message=message2, recipient=user1, read=False)
        notif3 = NotificationFactory(message=message2, recipient=user2, read=False)

        NotificationManager.mark_as_read(conversation, user1)

        notif1.refresh_from_db()
        notif2.refresh_from_db()
        notif3.refresh_from_db()

        assert notif1.read == True
        assert notif2.read == True
        assert notif3.read == False


    def test_conversation_unread_count_two_unread(self, user1, user2, conversation, message1, message2):
        NotificationFactory(message=message1, recipient=user1, read=False)
        NotificationFactory(message=message2, recipient=user1, read=False)
        NotificationFactory(recipient=user2, read=False)

        count = NotificationManager.conversation_unread_count(conversation, user1)

        assert count == 2


    def test_conversation_unread_count_one_unread(self, user1, user2, conversation, message1, message2):
        NotificationFactory(message=message1, recipient=user1, read=True)
        NotificationFactory(message=message2, recipient=user1, read=False)
        NotificationFactory(recipient=user2, read=False)
        
        count = NotificationManager.conversation_unread_count(conversation, user1)

        assert count == 1


    def test_other_conversations_count(self, user1, conversation, message1):
        user3 = ChatUserFactory()
        conversation2 = ConversationFactory(user1=user1, user2=user3)
        message2 = MessageFactory(conversation=conversation2, sender=user3)

        NotificationFactory(message=message1, recipient=user1, read=False)
        NotificationFactory(message=message2, recipient=user1, read=False)

        count = NotificationManager.other_conversations_count(conversation, user1)

        assert count == 1