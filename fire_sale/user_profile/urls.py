from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.CustomLoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile', views.edit_profile, name='profile'),
    path('logout', views.logout, name='logout')
]
