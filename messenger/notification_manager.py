from messenger.models import Notification

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

    # @staticmethod
    # def total_unread_count(user):