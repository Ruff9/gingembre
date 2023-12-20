import factory

from messenger.models import ChatUser, Conversation, Message
from utils.async_factory import AsyncFactory

class ChatUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ChatUser

    username = factory.Sequence(lambda n: "Agent %03d" % n)


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

# Async versions of factory
# factory_boy don't currently support async : https://github.com/FactoryBoy/factory_boy/issues/679

class AsyncChatUserFactory(AsyncFactory):
    class Meta:
        model = ChatUser

    username = factory.Sequence(lambda n: "Agent %03d" % n)


class AsyncConversationFactory(AsyncFactory):
    class Meta:
        model = Conversation

    user1 = factory.SubFactory(AsyncChatUserFactory)
    user2 = factory.SubFactory(AsyncChatUserFactory)