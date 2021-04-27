from django.shortcuts import render
from django.views.generic import View

from core.models import Product
from core.views.mixins import CategoryMixin


class HomeView(CategoryMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': self.get_categories(),  # 継承しているCategoryMixinのget_categoriesメソッドを実行
            'recommends': Product.objects.filter(is_recommended=True)[:3],  # 先頭から３つのデータを取得
            'new_arrivals': Product.objects.all().order_by('-pk')[:4],  # 末尾から４つのデータを取得
        }
        return render(request, 'core/home.html', context)
