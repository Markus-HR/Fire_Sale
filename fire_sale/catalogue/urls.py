from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="catalogue-index"),
    path('/bids', views.index, name="catalogue-mybids"),
]
