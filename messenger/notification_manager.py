from messenger.models import Conversation, Notification

class NotificationManager():

    @staticmethod
    def create(message, recipient):
        notification = Notification(message=message, recipient=recipient)
        notification.save()


    @staticmethod
    def mark_as_read(conversation, current_user):
        for message in conversation.message_set.all():
            message.notification_set.filter(recipient=current_user).update(read=True)


    @staticmethod
    def conversation_unread_count(conversation, current_user):
        messages = conversation.message_set.all()
        total = 0

        for message in messages:
            total += message.notification_set.filter(recipient=current_user, read=False).count()

        return total

    @staticmethod
    def total_unread_count(user):
        conversations = Conversation.objects.filter(user1=user) | Conversation.objects.filter(user2=user)
        total = 0

        for conversation in conversations:
            total += NotificationManager.conversation_unread_count(conversation, user)

        return total