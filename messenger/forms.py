from django import forms
from django.core.exceptions import ValidationError
from .models import ChatUser

class UserNameForm(forms.Form):
    username = forms.CharField(label="Choisir un pseudo", max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        if ChatUser.objects.filter(username=username).exists():
            raise ValidationError("username already exists")
        return username