from django.shortcuts import render, get_object_or_404

from main.models import Product, Category


def home(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Продукты для души и тела'
    }
    return render(request, 'home.html', context)

def products(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'Наши продукты'
    }
    return render(request, 'products.html', context)


def item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    context = {
        # 'object_list': Product.objects.filter(id=pk),
        'item': item,
        'cat_selected': item.category_id
    }
    return render(request, 'item.html', context)