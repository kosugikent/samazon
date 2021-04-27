from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import MajorCategory
from samazon_admin.forms import MajorCategoryCreateUpdateForm


class MajorCategoryListView(View):
    def get(self, request, *args, **kwargs):
        major_categories = MajorCategory.objects.all()
        return render(request, 'samazon_admin/major_category/list.html', {'major_categories': major_categories})


class MajorCategoryCreateView(View):
    def get(self, request, *args, **kwargs):
        form = MajorCategoryCreateUpdateForm()
        return render(request, 'samazon_admin/major_category/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MajorCategoryCreateUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:major_category_list')
        return render(request, 'samazon_admin/major_category/create.html', {'form': form})


class MajorCategoryDetailView(View):
    def get(self, request, *args, **kwargs):
        major_category = MajorCategory.objects.get(pk=kwargs['pk'])
        return render(request, 'samazon_admin/major_category/detail.html', {'major_category': major_category})


class MajorCategoryUpdateView(View):
    def get(self, request, *args, **kwargs):
        major_category = MajorCategory.objects.get(pk=kwargs['pk'])
        form = MajorCategoryCreateUpdateForm(instance=major_category)
        return render(request, 'samazon_admin/major_category/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        major_category = MajorCategory.objects.get(pk=kwargs['pk'])
        form = MajorCategoryCreateUpdateForm(request.POST, instance=major_category)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:major_category_list')
        return render(request, 'samazon_admin/major_category/update.html', {'form': form})


class MajorCategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        major_category = MajorCategory.objects.get(pk=kwargs['pk'])
        major_category.delete()
        return redirect('samazon_admin:major_category_list')

