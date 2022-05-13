from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.db.transaction import commit
from user_profile.models import UserProfile


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'placeholder': 'Username',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'bio',
            'profile_picture'
        )

    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(
            attrs={'placeholder': 'Bio',
                   'style': 'width: 18rem;'
                            'height: 15rem'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    profile_picture = forms.CharField(
        label='image',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'URL',
                   'style': 'width: 18rem;'
                            'height: 15rem'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def save(self, user):
        user_profile = super().save(commit=False)
        user_profile.user_id = user.id
        if commit:
            user_profile.save()
        return user_profile


class EditProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name'
        ]

    first_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Name',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class ImageForm(forms.Form):
    img = forms.ImageField()
