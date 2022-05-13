from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.index, name="item-index"),
    path('create_posting', views.create_posting, name="create-posting"),
    path('<int:id>/offers', views.view_offers, name='item-offers'),
    path('accept/<int:bidid>', views.accept_offer, name='accept-offer'),
]
