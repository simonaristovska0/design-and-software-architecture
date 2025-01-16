from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Remove default help texts for all fields
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Корисничко име",
        widget=TextInput())
    password = forms.CharField(
        label="Лозинка",
        widget=PasswordInput())
