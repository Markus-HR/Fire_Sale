from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="item-index"),
    path('create_posting', views.create_posting, name="create_posting")
]
