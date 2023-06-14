from django.urls import path

from .apps import MainConfig
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('product/', product, name='product')
]