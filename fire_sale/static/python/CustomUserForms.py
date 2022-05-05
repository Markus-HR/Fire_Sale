from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password',
                   'style': 'width: 300px;',
                   'class': 'form-control'}))
