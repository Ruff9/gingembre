from django.db import models

class ChatUser(models.Model):
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(ChatUser, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)