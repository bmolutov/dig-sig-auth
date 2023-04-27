from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


class CertificateLoginForm(forms.Form):
    certificate = forms.FileField(label='Certificate')


class BasicAuthLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
