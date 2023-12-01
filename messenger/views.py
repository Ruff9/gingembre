from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .forms import UserNameForm
from .models import ChatUser, Message


def index(request):
    current_chat_user = get_current_user(request)
    if current_chat_user is None:
        return HttpResponseRedirect(reverse("home"))

    user_list = ChatUser.objects.all().exclude(id=current_chat_user.id)

    return render(request, "messenger/index.html", {"current_user_name": current_chat_user.username, "user_list": user_list})


def room(request, room_name):
    return render(request, "messenger/room.html", {"room_name": room_name})


def home(request):
    if request.method == "POST":
        form = UserNameForm(request.POST)

        if form.is_valid():
            chat_user = ChatUser(username=form.cleaned_data['username'])
            chat_user.save()
            request.session["current_chat_user"] = chat_user.id
            return HttpResponseRedirect(reverse("index"))

    else:
        form = UserNameForm()

    return render(request, "messenger/home.html", {"form": form})


def conversation(request, username):
    current_user = get_current_user(request)
    if current_user is None:
        return HttpResponseRedirect(reverse("home"))

    contact = get_object_or_404(ChatUser, username=username)

    try:
        messages = Message.objects.filter(
            Q(sender=contact) & Q(receiver=current_user) |
            Q(sender=current_user) & Q(receiver=contact)
        )
    except Message.DoesNotExist:
        messages = None

    return render(request, "messenger/conversation.html", {"messages": messages, "contact_username": username})

def get_current_user(request):
    current_chat_user_id = request.session.get("current_chat_user")
    if current_chat_user_id is None:
        return
    else:
        return ChatUser.objects.get(pk=current_chat_user_id)

