from django.shortcuts import render

from main.models import Product


def home(request):
    return render(request, 'home.html')

def product(request):
    context = {
        'object_list': Product.objects.all(),

    }
    return render(request, 'product.html', context)
