from django.shortcuts import render, redirect, get_object_or_404
from catalogue.models import Ratings
from static.python.CustomUserForms import RegisterForm, LoginForm, EditProfileForm, ImageForm
from django.contrib.auth.views import LoginView
from user_profile.models import UserProfile


def register(request):
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


# def view_profile(request):
#     if UserProfile.objects.check(user_id=request.user.id):
#         user_profiles = UserProfile.objects.get(id=request.user.id)
#     else:
#         return edit_profile(request)
#
#     return render(request, 'user/view_profile.html', {
#         'user_profile': user_profiles
#     })


def edit_profile(request):
    instance = UserProfile.objects.filter(user_id=request.user.id)
    form2 = ImageForm()
    if request.method == 'POST':
        if instance:
            form = EditProfileForm(data=request.POST, instance=instance)
        else:
            form = EditProfileForm(data=request.POST)

        if form.is_valid():
            form.save(request.user)
            return redirect('user/view_profile.html')
    else:
        if instance:
            form = EditProfileForm(instance=instance)
        else:
            form = EditProfileForm()

    return render(request, 'user/edit_profile.html', {
        'form': form,
        'form2': form2
    })


class CustomLoginView(LoginView):
    form_class = LoginForm


def calc_rating(request):
    user_id = request.user.id
    # ratings = Ratings.objects.get(user_id=user_id)
    ratings = Ratings.objects.all()
    temp = []
    for rating in ratings:
        if rating.user_id == user_id:
            temp.push(rating)
    return {'ratings': temp}
