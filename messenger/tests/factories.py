import factory

from messenger.models import ChatUser, Conversation, Message


class ChatUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatUser

    username = 'factory_chat_user'


class ConversationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Conversation

    user1 = factory.SubFactory(ChatUserFactory)
    user2 = factory.SubFactory(ChatUserFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    conversation = factory.SubFactory(ConversationFactory)
    sender = factory.SubFactory(ChatUserFactory)
    content = "lorem ipsum"
