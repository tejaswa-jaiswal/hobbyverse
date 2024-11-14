from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from home import views
urlpatterns = [
   path("", views.index, name = "index"),
   path("login_user", views.login_user, name = "login_user"),
   path("register", views.register, name = "register"),
   path("intrests", views.intrests, name= "intrests"),
   path("logout", views.logout_user, name = "logout"),
   path("community_search" , views.community_search, name="community_search"),
   path("profile", views.index, name = "profile"),
   path("add_community", views.add_community, name = "add_community"),
]