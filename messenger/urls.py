from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("get_conversation/<str:user_id>/", views.get_conversation, name="get_conversation")
]
