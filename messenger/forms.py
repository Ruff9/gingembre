from django import forms


class UserNameForm(forms.Form):
    username = forms.CharField(label="Choisir un pseudo", max_length=30)