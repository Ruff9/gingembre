import factory

from messenger.models import ChatUser


class ChatUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatUser

    username = 'factory_chat_user'
