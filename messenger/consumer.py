import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from messenger.models import Conversation, Message, ChatUser, Notification
from messenger.notification_manager import NotificationManager

class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.current_user_id = self.scope["url_route"]["kwargs"]["current_user_id"]
        self.conv_group_name = f"conv_{self.conversation_id}"

        self.conversation = Conversation.objects.get(pk=self.conversation_id)
        self.current_user = ChatUser.objects.get(pk=self.current_user_id)

        async_to_sync(self.channel_layer.group_add)(
            self.conv_group_name, self.channel_name
        )

        NotificationManager.mark_as_read(self.conversation, self.current_user)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.conv_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json["message"]
        sender_id = text_data_json["sender_id"]
        sender = ChatUser.objects.get(pk=sender_id)

        message = Message(conversation=self.conversation, content=message_content, sender=sender)
        message.save()

        if self.conversation.user1 == sender:
            recipient = self.conversation.user2
        else:
            recipient = self.conversation.user1

        NotificationManager.create(message, recipient)

        async_to_sync(self.channel_layer.group_send)(
            self.conv_group_name, {
                "type": "chat.message",
                "message": message_content,
                "sender_id": sender_id
            }
        )

    def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        self.send(text_data=json.dumps({"message": message, "sender_id": sender_id}))
