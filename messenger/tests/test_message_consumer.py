import pytest
import pytest_asyncio
import json

from django.urls import path
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async

from messenger.consumer import MessageConsumer
from messenger.models import Message
from factories import AsyncConversationFactory, AsyncChatUserFactory


@pytest.fixture(autouse=True)
def use_test_channel_layer(settings):
    settings.CHANNEL_LAYERS = {
        'default': { 'BACKEND': 'channels.layers.InMemoryChannelLayer' }
    }


@pytest_asyncio.fixture
async def setup():
    user = await AsyncChatUserFactory()
    conversation = await AsyncConversationFactory(user1=user)
    application = URLRouter([
        path("ws/conversation/<conversation_id>/", MessageConsumer.as_asgi()),
    ])

    yield user, conversation, application

    await sync_to_async(user.delete)()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestMessageConsumer:
    async def test_can_connect_to_server(self, setup):
        _, conversation, application = setup

        communicator = WebsocketCommunicator(application, f"/ws/conversation/{conversation.id}/")
        connected, _ = await communicator.connect()
        assert connected

        await communicator.disconnect()

    async def test_sends_and_receive_messages(self, setup):
        user, conversation, application = setup

        communicator = WebsocketCommunicator(application, f"/ws/conversation/{conversation.id}/")
        await communicator.connect()

        message = {
            "message": "Yo",
            "sender_id": user.id
        }

        await communicator.send_json_to(message)
        response = await communicator.receive_from()
        assert response == json.dumps(message)

        message = await sync_to_async(Message.objects.latest)()
        assert message.content == "Yo"

        await communicator.disconnect()

    async def test_sends_message_to_channel_layer(self, setup):
        user, conversation, application = setup

        communicator = WebsocketCommunicator(application, f"/ws/conversation/{conversation.id}/")
        await communicator.connect()

        channel_layer = get_channel_layer()
        assert channel_layer != None

        channel_name = list(channel_layer.channels.keys())[0]

        message = {
            "type": "chat.message",
            "message": "Bien ou quoi",
            "sender_id": user.id
        }

        await channel_layer.send(channel_name, message)
        response = await communicator.receive_from()

        assert response == json.dumps({"message": "Bien ou quoi", "sender_id": user.id})

        await communicator.disconnect()
