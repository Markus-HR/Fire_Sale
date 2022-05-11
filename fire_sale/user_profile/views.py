from django.shortcuts import render, redirect
from static.python.CustomUserForms import RegisterForm, LoginForm, EditProfileForm, ImageForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as LogoutUser
from user_profile.models import UserProfile


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {
        'form': form
    })


def logout(request, *args, **kwargs):
    LogoutUser(request)
    return redirect('login')


def edit_profile(request, *args, **kwargs):
    if UserProfile.objects.filter(user_id=request.user.id).exists():
        instance = UserProfile.objects.filter(user_id=request.user.id)[0]
        if request.method == 'POST':
            form = EditProfileForm(data=request.POST, instance=instance)
            if form.is_valid():
                form.save(request.user)
                return redirect('profile')
        else:
            form = EditProfileForm(instance=instance)
    else:
        if request.method == 'POST':
            form = EditProfileForm(data=request.POST)
            if form.is_valid():
                form.save(request.user)
                return redirect('profile')
        else:
            form = EditProfileForm()

    return render(request, 'user/edit_profile.html', {
        'form': form,
    })


class CustomLoginView(LoginView):
    form_class = LoginForm


