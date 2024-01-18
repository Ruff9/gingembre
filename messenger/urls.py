from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("index/", views.index, name="index"),
    path("conversation/<int:conversation_id>/", views.conversation, name="conversation")
]
