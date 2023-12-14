# scripts/clear_chat_users.py

from messenger.models import ChatUser
from django.contrib.sessions.models import Session


def run():
    ChatUser.objects.all().delete()
    Session.objects.all().delete()

    print("Chat users deleted and session cleared.")