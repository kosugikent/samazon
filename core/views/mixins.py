from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from core.models import Category


class LoginRequiredMixin(BaseLoginRequiredMixin):
    login_url = reverse_lazy('core:login')


class CategoryMixin:
    def get_categories(self):
        categories = {}
        for category in Category.objects.all():
            # categories辞書のキーにmajor_category_nameが存在しない場合、デフォルト値として空のリストを追加しておく
            categories.setdefault(category.major_category.name, [])
            # 同じmajor_category_nameのcategoryをリストに追加していく
            categories[category.major_category.name].append(category)
        return categories.items()


class PaginationMixin:
    paginate_by = 3

    def get_page_data(self, queryset):
        paginator = Paginator(queryset, self.paginate_by)
        # URLにpageパラメータがない場合は、デフォルト値として1を使用する
        page_number = self.request.GET.get('page', 1)
        page = paginator.page(page_number)
        return {
            'paginator': paginator,
            'page_obj': page,
            'object_list': page.object_list
        }
