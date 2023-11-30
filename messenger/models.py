from django.db import models

class ChatUser(models.Model):
    username = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
