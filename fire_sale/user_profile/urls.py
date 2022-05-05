from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    # path('login', views.CustomLoginView.as_view(template_name='user/login.html'), name='login')
    path('login', LoginView.as_view(template_name='user/login.html'), name='login')
]
