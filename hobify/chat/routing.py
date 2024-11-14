from django.urls import path
from .consumers import *
from .routing import ChatroomConsumer
websocket_urlpatterns=[
    path("ws/chatroom/<str:curr_channel>", ChatroomConsumer.as_asgi()),
]