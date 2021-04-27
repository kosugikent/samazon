from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import Category, Product
from core.views.mixins import CategoryMixin, PaginationMixin


class ProductListView(CategoryMixin, PaginationMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(pk=kwargs['pk'])
        # URLにorder_byパラメータがない場合は、idの昇順で並び替える
        products = category.products.all().order_by(request.GET.get('order_by', 'id'))
        context = {
            'category': category,
            'categories': self.get_categories(),  # 継承しているCategoryMixinのget_categoriesメソッドを実行
            **self.get_page_data(products)  # 継承しているPaginationMixinのget_page_dataメソッドを実行
        }
        return render(request, 'core/product/list.html', context)


class ProductDetailView(CategoryMixin, PaginationMixin, View):
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        favorite_added = request.user.is_authenticated and request.user.favorites.filter(product=product).exists()
        context = {
            'product': product,
            'categories': self.get_categories(),  # 継承しているCategoryMixinのget_categoriesメソッドを実行
            'favorite_added': favorite_added,
            **self.get_page_data(product.reviews.all()),  # 継承しているPaginationMixinのget_page_dataメソッドを実行
        }
        return render(request, 'core/product/detail.html', context)


class ProductReviewView(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        product.reviews.create(
            user=request.user,
            score=request.POST['score'],
            body=request.POST['body']
        )
        return redirect('core:product_detail', product.pk)
