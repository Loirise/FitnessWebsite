from django import forms
from django.contrib.auth.models import User


class UserSignUpForm(forms.Form):
    username = forms.CharField(required=True, max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['password'],
            self.cleaned_data['email'],
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name']
        )
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput())