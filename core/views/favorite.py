from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import Favorite


class FavoriteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/favorite.html')


class FavoriteAddDeleteView(View):
    def post(self, request, *args, **kwargs):
        favorite, added = Favorite.objects.get_or_create(
            user=request.user,
            product_id=request.POST['product_id']
        )
        if not added:
            favorite.delete()
        return redirect('core:product_detail', request.POST['product_id'])


class FavoriteDeleteView(View):
    def post(self, request, *args, **kwargs):
        Favorite.objects.filter(pk__in=request.POST.getlist('favorite_ids[]')).delete()
        return JsonResponse({})
