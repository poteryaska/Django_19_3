
from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import MainConfig
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>/item/', cache_page(60)(ItemDetailView.as_view()), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/edit/<slug:slug>', BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/delete/<slug:slug>', BlogDeleteView.as_view(), name='blog_delete'),
]