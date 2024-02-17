from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from useraccount.models import UserAccount

class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ("email", "password")

    def clean(self):
        """ validates login_form credentials"""

        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login")

