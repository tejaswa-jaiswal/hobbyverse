from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from chat import views
urlpatterns = [
   path("channel/<int:community_Id>", views.channel, name = "channel"),
   path("add_channel", views.add_channel , name="add_channel"),
   path("add_channel/<int:community_Id>/<slug:username>", views.add_channel , name="add_channel"),
   path("get_chat", views.get_chat, name="get_chat"),
   path("current_channel/<int:channel_ID>", views.current_channel, name="current_channel"),
]