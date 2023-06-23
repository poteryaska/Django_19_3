
from django.urls import path

from .apps import MainConfig
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/item/', ItemDetailView.as_view(), name='product_detail'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/edit/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/delete/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
]