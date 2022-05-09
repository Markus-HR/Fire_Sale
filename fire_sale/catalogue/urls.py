from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="catalogue-index"),
    path('bids', views.my_bids, name="catalogue-bids"),
    path('postings', views.my_postings, name="catalogue-postings"),
]
