import pytest

from messenger.models import Notification
from messenger.notification_manager import NotificationManager
from factories import ChatUserFactory, ConversationFactory, MessageFactory, NotificationFactory


@pytest.mark.django_db
class TestNotificationManager:
    def test_create(self):
        user = ChatUserFactory()
        message = MessageFactory()

        NotificationManager.create(message, user)

        notification = Notification.objects.latest()

        assert notification.recipient_id == user.id
        assert notification.message_id == message.id


    def test_mark_as_read(self):
        user1 = ChatUserFactory()
        user2 = ChatUserFactory()
        conversation = ConversationFactory(user1=user1, user2=user2)
        message1 = MessageFactory(conversation=conversation)
        message2 = MessageFactory(conversation=conversation)

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


    def test_conversation_unread_count_two_unread(self):
        user1 = ChatUserFactory()
        user2 = ChatUserFactory()
        conversation = ConversationFactory(user1=user1, user2=user2)
        
        message1 = MessageFactory(conversation=conversation)
        message2 = MessageFactory(conversation=conversation)
        NotificationFactory(message=message1, recipient=user1, read=False)
        NotificationFactory(message=message2, recipient=user1, read=False)
        NotificationFactory(recipient=user2, read=False)

        count = NotificationManager.conversation_unread_count(conversation, user1)

        assert count == 2


    def test_conversation_unread_count_one_unread(self):
        user1 = ChatUserFactory()
        user2 = ChatUserFactory()
        conversation = ConversationFactory(user1=user1, user2=user2)

        message1 = MessageFactory(conversation=conversation)
        message2 = MessageFactory(conversation=conversation)
        NotificationFactory(message=message1, recipient=user1, read=True)
        NotificationFactory(message=message2, recipient=user1, read=False)
        NotificationFactory(recipient=user2, read=False)
        
        count = NotificationManager.conversation_unread_count(conversation, user1)

        assert count == 1
