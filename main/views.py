from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.conf import settings

from main.models import Product, Category, Blog

class HomeView(generic.TemplateView):
    template_name = 'main/home.html'
    extra_context = {
        'title': 'Продукты для души и тела'
    }

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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

class BlogDetailView(generic.DetailView):
    model = Blog
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_view += 1
        self.object.save()
        if self.object.count_view == 10:
            send_mail(
                "Поздравляем",
                f"Количество просмотров:{self.object.count_view}",
                settings.EMAIL_HOST_USER,
                ["jane87.05@mail.ru"],
            )

        return self.object

class BlogCreateView(generic.CreateView):
    model = Blog
    fields = ('name', 'description', "is_published", "photo",)
    success_url = reverse_lazy('main:blog_list')

class BlogUpdateView(generic.UpdateView):
    model = Blog
    fields = ('name', 'description', "is_published", "photo",)

    def get_success_url(self):
        return reverse('main:blog_detail', args=[self.kwargs.get('slug')])
class BlogDeleteView(generic.DeleteView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')