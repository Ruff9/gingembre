from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .forms import UserNameForm
from .models import ChatUser, Message, Conversation


def index(request):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    user_list = ChatUser.objects.all().exclude(id=current_user.id)

    return render(request, "messenger/index.html", {"current_user_name": current_user.username, "user_list": user_list})


def home(request):
    current_user = get_current_user(request)
    if current_user: return redirect("index")

    if request.method == "POST":
        form = UserNameForm(request.POST)

        if form.is_valid():
            chat_user = ChatUser(username=form.cleaned_data['username'])
            chat_user.save()
            request.session["current_user"] = chat_user.id
            return redirect("index")

    else:
        form = UserNameForm()

    return render(request, "messenger/home.html", {"form": form})


def get_conversation(request, username):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    contact = ChatUser.objects.get(username=username)

    try:
        conversation = Conversation.objects.get(
            Q(user1=contact) & Q(user2=current_user) |
            Q(user1=current_user) & Q(user2=contact)
        )
    except Conversation.DoesNotExist:
        conversation = Conversation(user1=current_user, user2=contact)
        conversation.save()

    return redirect("conversation", conversation_id=conversation.id)


def conversation(request, conversation_id):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    conversation = get_object_or_404(Conversation, pk=conversation_id)

    if conversation.user1 == current_user:
        contact = conversation.user2
    else:
        contact = conversation.user1

    messages = conversation.message_set.all()

    return render(request, "messenger/conversation.html", {
        "conversation_id": conversation_id,
        "messages": messages,
        "contact_username": contact.username,
        "current_user_id": current_user.id
    })


def get_current_user(request):
    current_user_id = request.session.get("current_user")
    if current_user_id is None:
        return
    else:
        return ChatUser.objects.get(pk=current_user_id)
