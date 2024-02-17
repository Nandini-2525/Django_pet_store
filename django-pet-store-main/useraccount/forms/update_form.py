from django import forms
from useraccount.models import UserAccount

class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ("email", "first_name", "last_name", "phone_number")

    def clean_email(self):
        """ Validates that email is unique """

        if self.is_valid():
            email = self.cleaned_data["email"]
            try:
                account = UserAccount.objects.exclude(pk=self.instance.pk).get(email=email)
            except UserAccount.DoesNotExist:
                return email
            raise forms.ValidationError(f"email {email} is already is use")
