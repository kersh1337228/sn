from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(
        r'chats/private_chat/(?P<chat_id>\w+)/$',
        consumers.MessageConsumer.as_asgi(),
    ),
]