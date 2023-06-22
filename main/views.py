
from django.shortcuts import render, get_object_or_404
from django.views import generic

from main.models import Product, Category, Blog


def home(request):
    context = {
        'title': 'Продукты для души и тела'
    }
    return render(request, 'main/home.html', context)

class ProductListView(generic.ListView):
    model = Product
    extra_context = {
        'title': 'Наши продукты'
    }

class CategoryListView(generic.ListView):
    model = Category
    extra_context = {
        'title': 'Категории продуктов'
    }
class ItemDetailView(generic.DetailView):
    model = Product

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data['title'] = context_data['object']
    #     return context_data

class BlogListView(generic.ListView):
    model = Blog
    extra_context = {
        'title': 'Пишем о еде'
    }

class BlogDetailView(generic.DetailView):
    model = Blog