from django.db import models


class ChatUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    user1 = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="user2")


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_at"


class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = "created_at"