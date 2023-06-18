import products as products
from django.urls import path

from .apps import MainConfig
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('<int:pk>/item/', item, name='item')
]