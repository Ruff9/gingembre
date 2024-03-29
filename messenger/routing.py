from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/conversation/(?P<conversation_id>\w+)/current_user/(?P<current_user_id>\w+)/$", consumer.MessageConsumer.as_asgi())
]