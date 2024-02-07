from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q, Count
from django.http import JsonResponse

from .forms import UserNameForm
from .models import ChatUser, Message, Conversation
from .notification_manager import NotificationManager


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


def index(request):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    user_list = ChatUser.objects.all().exclude(id=current_user.id)

    return render(request, "messenger/index.html", {
        "current_user_name": current_user.username,
        "current_user_id": current_user.id,
    })


def conversation(request, conversation_id):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    conversation = get_object_or_404(Conversation, pk=conversation_id)
    contact = conversation.user2 if conversation.user1 == current_user else conversation.user1

    return render(request, "messenger/conversation.html", {
        "conversation_id": conversation_id,
        "messages": conversation.message_set.all().order_by('created_at'),
        "contact_username": contact.username,
        "current_user_id": current_user.id
    })


def conversation_index(request):
    current_user = get_current_user(request)
    conversations = dict()
    if current_user is None: return JsonResponse(conversations)

    user_list = ChatUser.objects.all().exclude(id=current_user.id)

    if not user_list:
        return JsonResponse(conversations)
    else:
        for count, user in enumerate(user_list, start=1):
            conversation = get_or_create_conversation(current_user, user)
            url = reverse('conversation', kwargs={'conversation_id': conversation.id})
            contact_name = user.username
            notification_count = NotificationManager.conversation_unread_count(conversation, current_user)
            data = dict(id = count, conversation_id = conversation.id, url = url, contact_name = contact_name, notification_count = notification_count)
            conversations[count] = data

        return JsonResponse(conversations)


def notification_count(request, conversation_id):
    current_user = get_current_user(request)
    if current_user is None: return redirect("home")

    conversation = Conversation.objects.get(pk=conversation_id)
    total = NotificationManager.other_conversations_count(conversation, current_user)

    return JsonResponse({ "total": total })


def get_current_user(request):
    current_user_id = request.session.get("current_user")
    if current_user_id is None:
        return
    else:
        return ChatUser.objects.get(pk=current_user_id)


def get_or_create_conversation(current_user, contact):
    try:
        conversation = Conversation.objects.get(
            Q(user1=contact) & Q(user2=current_user) |
            Q(user1=current_user) & Q(user2=contact)
        )
    except Conversation.DoesNotExist:
        conversation = Conversation(user1=current_user, user2=contact)
        conversation.save()

    return conversation
