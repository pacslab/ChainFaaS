from django import forms
from django.contrib.auth.models import User
from profiles.models import Provider, Developer


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    is_developer = forms.BooleanField(label="Do you want to be a provider?", required=False)
    is_provider = forms.BooleanField(label="Do you want to be a developer?", required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ChangeInfoForm(forms.ModelForm):
    is_developer = forms.BooleanField(required=False)
    is_provider = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email')
