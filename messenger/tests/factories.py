import factory

from messenger.models import ChatUser, Message


class ChatUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatUser

    username = 'factory_chat_user'


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    body = "lorem ipsum"
    sender = factory.SubFactory(ChatUserFactory)
    receiver = factory.SubFactory(ChatUserFactory)