from django.contrib import admin
from django.contrib.auth.models import Group
from .models import ChatUser


class ChatUserAdmin(admin.ModelAdmin):
    model = ChatUser
    fields = ["username", "created_at"]
    list_display = ["username", "created_at"]

admin.site.register(ChatUser)
