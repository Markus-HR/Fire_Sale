from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path('create_bid', views.create_bid, name="create_bid")
]
