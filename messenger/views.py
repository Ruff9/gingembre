from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import UserNameForm
from .models import ChatUser


def index(request):
    return render(request, "messenger/index.html")


def room(request, room_name):
    return render(request, "messenger/room.html", {"room_name": room_name})


def home(request):
    if request.method == "POST":
        form = UserNameForm(request.POST)

        if form.is_valid():
            chat_user = ChatUser(username=form.cleaned_data['username'])
            chat_user.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = UserNameForm()

    return render(request, "messenger/home.html", {"form": form})
