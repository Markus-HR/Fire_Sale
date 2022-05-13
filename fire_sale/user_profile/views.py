from statistics import mean
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from catalogue.models import Ratings, Postings, Bids
from static.python.CustomUserForms import RegisterForm, LoginForm, EditProfileForm, EditProfileUserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as LogoutUser
from user_profile.models import UserProfile


def register(request, *args, **kwargs):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = user.username
            user.save()

            user_profile = UserProfile()
            user_profile.user = user
            user_profile.save()
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
    user = request.user
    if UserProfile.objects.filter(user_id=request.user.id).exists():
        instance = UserProfile.objects.filter(user_id=request.user.id)[0]
        if request.method == 'POST':
            form = EditProfileForm(data=request.POST, instance=instance)
            user_form = EditProfileUserForm(data=request.POST, instance=user)
            if form.is_valid() and user_form.is_valid():
                form.save(request.user)
                user_form.save()
                return redirect('profile')
        else:
            form = EditProfileForm(instance=instance)
            user_form = EditProfileUserForm(instance=user)
    else:
        if request.method == 'POST':
            form = EditProfileForm(data=request.POST)
            user_form = EditProfileUserForm(data=request.POST, instance=user)
            if form.is_valid() and user_form.is_valid():
                form.save(request.user)
                user_form.save()
                return redirect('profile')
        else:
            form = EditProfileForm()
            user_form = EditProfileUserForm(instance=user)

    return render(request, 'user/edit_profile.html', {
        'form': form,
        'user_form': user_form,
    })


def view_profile(request, userid):
    user = get_object_or_404(User, pk=userid)
    user_profile = get_user_profile(userid)
    return render(request, 'user/view_profile.html', {
        'user': user,
        'userProfile': user_profile,
        'userRating': calculate_user_rating(userid),
        'data': get_post_item(userid)
    })


def get_user_profile(userid):
    profile_set = UserProfile.objects.all()
    for profile in profile_set.iterator():
        if profile.user_id == userid:
            return profile
    return None


def calculate_user_rating(u_id):
    ratings = Ratings.objects.filter(user_id=u_id)
    rating_score = 0
    if len(ratings) > 0:
        rating_score = mean([x.rating for x in ratings])
    return str(round(rating_score))


def get_user_posts(userid):
    user_posts = []
    post_set = Postings.objects.all()
    for post in post_set.iterator():
        if post.user_id == userid:
            user_posts.append(post)
    return user_posts


def get_post_item(userid):
    posts = get_user_posts(userid)
    post_item = [{
        'name': x.item.name,
        'item_pic': x.item.image1,
        'max_bid': max([y.price for y in Bids.objects.filter(posting_id=x.id)], default=0),
        'category': x.item.category.name,
        'date': x.creation_date,
        'open': x.open,
        'has_accepted_bid': check_accepted_bid(x.id)[0],
        'itemid': x.item_id
    } for x in posts]
    return post_item


def check_accepted_bid(post_id):
    bids = Bids.objects.filter(posting_id=post_id, accept=True)
    if bids:
        return [True, [x.price for x in bids]]
    else:
        return [False, [0]]


class CustomLoginView(LoginView):
    form_class = LoginForm


