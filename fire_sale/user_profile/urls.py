from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.CustomLoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile', views.edit_profile, name='profile'),
    path('calc_rating', views.calc_rating, name='calc_rating')
]
