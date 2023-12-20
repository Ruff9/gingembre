import pytest
import json

from django.urls import path
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async

from messenger.consumer import MessageConsumer
from messenger.models import Message
from factories import AsyncConversationFactory, AsyncChatUserFactory


TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@pytest.mark.asyncio
@pytest.mark.django_db
class TestMessageConsumer:
    async def test_sends_and_receive_messages(self):
        user1 = await AsyncChatUserFactory()
        user2 = await AsyncChatUserFactory()
        conversation = await AsyncConversationFactory(user1=user1, user2=user2)

        application = URLRouter([
            path("ws/conversation/<conversation_id>/", MessageConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(application, f"/ws/conversation/{conversation.id}/")
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({"message": "Yo", "sender_id": user1.id})
        response = await communicator.receive_from()
        assert response == json.dumps({"message": "Yo", "sender_id": user1.id})

        message = await sync_to_async(Message.objects.latest)()
        assert message.content == "Yo"

        await communicator.disconnect()

    async def test_sends_message_to_channel_layer(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user1 = await AsyncChatUserFactory()
        user2 = await AsyncChatUserFactory()
        conversation = await AsyncConversationFactory(user1=user1, user2=user2)

        application = URLRouter([
            path("ws/conversation/<conversation_id>/", MessageConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(application, f"/ws/conversation/{conversation.id}/")
        await communicator.connect()

        channel_layer = get_channel_layer()
        assert channel_layer != None

        channel_name = list(channel_layer.channels.keys())[0]

        message = {
            "type": "chat.message",
            "message": "Bien ou quoi",
            "sender_id": user1.id
        }

        await channel_layer.send(channel_name, message)
        response = await communicator.receive_from()

        assert response == json.dumps({"message": "Bien ou quoi", "sender_id": user1.id})

        # message = await sync_to_async(Message.objects.latest)()
        # assert message.content == "Bien ou quoi"

        await communicator.disconnect()
