from django.urls import re_path

from .consumer import Chating

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", Chating.as_asgi()),
]
