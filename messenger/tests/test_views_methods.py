# import pytest
# from messenger.views import count_notifications
# from factories import ConversationFactory, MessageFactory, NotificationFactory


# @pytest.mark.django_db
# class TestCountNotifications:
#     def test_one_unread_message(self):
#         conversation = ConversationFactory()
#         message = MessageFactory(conversation=conversation)
#         NotificationFactory(message=message, read=False)

#         assert count_notifications(conversation) == 1

#     def test_one_read_message(self):
#         conversation = ConversationFactory()
#         message = MessageFactory(conversation=conversation)
#         NotificationFactory(message=message, read=True)

#         assert count_notifications(conversation) == 0

#     def test_two_unread_messages(self):
#         conversation = ConversationFactory()
#         message1 = MessageFactory(conversation=conversation)
#         message2 = MessageFactory(conversation=conversation)
#         NotificationFactory(message=message1, read=False)
#         NotificationFactory(message=message2, read=False)
        
#         assert count_notifications(conversation) == 2

#     def test_one_read_message_and_one_unread(self):
#         conversation = ConversationFactory()
#         message1 = MessageFactory(conversation=conversation)
#         message2 = MessageFactory(conversation=conversation)
#         NotificationFactory(message=message1, read=True)
#         NotificationFactory(message=message2, read=False)
        
#         assert count_notifications(conversation) == 1
