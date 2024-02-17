from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from useraccount.models import UserAccount
from pet_store import settings


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. please provide email address")

    class Meta:
        model = UserAccount
        fields = ("email", "password1", "password2", "phone_number", "address", "surburb", "city")
