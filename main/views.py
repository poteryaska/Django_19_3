from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.conf import settings
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from main.forms import ProductForm, VersionForm
from main.models import Product, Category, Blog, Version


class HomeView(generic.TemplateView):
    template_name = 'main/home.html'
    extra_context = {
        'title': 'Продукты для души и тела'
    }

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    extra_context = {
        'title': 'Категории продуктов'
    }

class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    extra_context = {
        'title': 'Наши продукты'
    }


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Product
    permission_required = 'main.view_product'
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("You are not owner of this product!")
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_version = self.get_object()

        context["product_version"] = product_version.active_version
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if self.request.user is None:
            raise Http404("You can't create a new product!")

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')
    permission_required = (
        'main.publish_status',
        'main.change_description',
        'main.change_category',
    )


    def has_permission(self):
        perms = self.get_permission_required()
        product: Product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perms(perms)

    def get_form(self, **kwargs):
        form = super().get_form()
        # if self.request.user != form.instance.owner:
        enabled_fields = set()
        if self.request.user.has_perm('main.change_category'):
            enabled_fields.add('category')
        if self.request.user.has_perm('main.change_description'):
            enabled_fields.add('description')
        if self.request.user.has_perm('main.publish_status'):
            enabled_fields.add('is_published')
        for field_name in enabled_fields.symmetric_difference(form.fields):
            form.fields[field_name].disabled = True
            form.errors.pop(field_name, None)

        return form

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            # before add new version make other version - inactive
            versions = Version.objects.all()
            for ver in versions:
                ver.is_active = False
                ver.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("You are not owner of this product!")
        return self.object

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('main:product_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("You are not owner of this product!")
        return self.object

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