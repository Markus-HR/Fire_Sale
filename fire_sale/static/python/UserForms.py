from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password']

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if password != self.data['password2']:
            raise forms.ValidationError('Passwords dont match!')
        return password


class UserLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password',
                   'style': 'width: 18rem;',
                   'class': 'form-control'}
        )
    )
