from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))
