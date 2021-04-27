from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import Category
from samazon_admin.forms import CategoryCreateUpdateForm


class CategoryListView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'samazon_admin/category/list.html', {'categories': categories})


class CategoryCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CategoryCreateUpdateForm()
        return render(request, 'samazon_admin/category/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CategoryCreateUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:category_list')
        return render(request, 'samazon_admin/category/create.html', {'form': form})


class CategoryDetailView(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        return render(request, 'samazon_admin/category/detail.html', {'category': category})


class CategoryUpdateView(View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        form = CategoryCreateUpdateForm(instance=category)
        return render(request, 'samazon_admin/category/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        form = CategoryCreateUpdateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:category_list')
        return render(request, 'samazon_admin/category/update.html', {'form': form})


class CategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        category.delete()
        return redirect('samazon_admin:category_list')
