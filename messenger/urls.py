from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.index, name="index"),
    path("get_conversation/<str:username>/", views.get_conversation, name="get_conversation"),
    path("conversation/<int:conversation_id>/", views.conversation, name="conversation")
]
