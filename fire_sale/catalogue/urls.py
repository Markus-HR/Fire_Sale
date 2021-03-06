from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="catalogue-index"),
    path('bids', views.my_bids, name="catalogue-bids"),
    path('bids/accepted', views.my_accepted_bids, name="catalogue-accepted-bids"),
    path('postings', views.my_postings, name="catalogue-postings"),
    path('<int:id>/checkout', views.checkout, name='checkout'),
    path('<int:id>/session_checkout', views.session_checkout, name='session_checkout'),
    path('<int:id>/checkout_review', views.checkout_review, name='checkout_review'),
    path('bid_history', views.bid_history, name='bid_history'),
]
