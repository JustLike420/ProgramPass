from django.contrib import admin
from django.urls import path


from .views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='item_list'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('about/', about, name='about'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
]