from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from core.models import Cart


class CartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/cart.html')


class CartAddView(View):
    def post(self, request, *args, **kwargs):
        cart, added = Cart.objects.get_or_create(
            defaults={'qty': request.POST['qty']},
            user=request.user,
            product_id=request.POST['product_id']
        )
        if not added:
            cart.qty += int(request.POST['qty'])
            cart.save()
        return redirect('core:product_detail', request.POST['product_id'])


class CartUpdateView(View):
    def post(self, request, *args, **kwargs):
        Cart.objects.filter(pk=kwargs['pk']).update(qty=request.POST['qty'])
        return redirect('core:cart')


class CartDeleteView(View):
    def post(self, request, *args, **kwargs):
        Cart.objects.filter(pk__in=request.POST.getlist('cart_ids[]')).delete()
        return JsonResponse({})
