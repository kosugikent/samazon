from django.db.models import Avg, Q
from django.shortcuts import render
from django.views.generic import View

from core.models import Product
from core.views.mixins import CategoryMixin, PaginationMixin


class SearchView(CategoryMixin, PaginationMixin, View):
    def get(self, request, *args, **kwargs):
        # 検索用パラメータを表すQオブジェクト
        q = Q()
        for param_name, value in request.GET.items():
            if not value:
                continue
            if param_name == 'search_word':
                # プロダクト名に検索ワードが部分一致するか
                q &= Q(name__contains=value)
            elif param_name == 'category_name':
                # プロダクトのカテゴリーに一致するか
                q &= Q(category__name=value)
            elif param_name == 'star':
                # プロダクトのレビューの星がリクエスト値以上か
                q &= Q(star__gte=value)

        # valuesメソッドにより、プロダクトのpkでレコードをグループ化する。
        # annotateメソッドにより、レビューのスコアの平均値を求める。
        # Qオブジェクトにより、レコードをフィルターする。
        products = Product.objects.values('pk').annotate(star=Avg('reviews__score')).filter(q)

        # フィルター後にproductsに代入されているのはQuerySetではないので、フィルター後に残ったプロダクトのidにより、QuerySetを取得する
        products = Product.objects.filter(pk__in=[p['pk'] for p in products])

        context = {
            'categories': self.get_categories(),
            **self.get_page_data(products)
        }
        return render(request, 'core/search.html', context)
