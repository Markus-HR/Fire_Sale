from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match."
    }

    email = forms.EmailField(
        validators=['validate_user'],
        widget=forms.EmailInput(
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

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user

    def validate(self):
        self.validate_user()
        self.validate_password()

    def validate_password(self):
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise ValidationError

    def clean_user(self, *args, **kwargs):
        if User.objects.exclude(pk=self.instance.pk).filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
