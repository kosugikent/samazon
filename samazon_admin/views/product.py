from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import Product
from core.views.mixins import PaginationMixin
from samazon_admin.forms import ProductCreateUpdateForm


class ProductListView(PaginationMixin, View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        if 'keyword' in request.GET:
            products = products.filter(name__contains=request.GET['keyword'])
        products = products.order_by(request.GET.get('order_by', 'pk'))
        context = self.get_page_data(products)
        return render(request, 'samazon_admin/product/list.html', context)


class ProductCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ProductCreateUpdateForm()
        return render(request, 'samazon_admin/product/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        # request.FILESにブラウザから送られてきた画像が入っている
        form = ProductCreateUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:product_list')
        return render(request, 'samazon_admin/product/create.html', {'form': form})


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        return render(request, 'samazon_admin/product/detail.html', {'product': product})


class ProductUpdateView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        form = ProductCreateUpdateForm(instance=product)
        return render(request, 'samazon_admin/product/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        # request.FILESにブラウザから送られてきた画像が入っている
        form = ProductCreateUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('samazon_admin:product_list')
        return render(request, 'samazon_admin/product/update.html', {'form': form})


class ProductDeleteView(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        product.delete()
        return redirect('samazon_admin:product_list')
