import stripe
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View

from core.forms.mypage import AddressUpdateForm
from core.models import User
from core.views.mixins import LoginRequiredMixin


class MyPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/mypage.html')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/profile_update.html')

    def post(self, request, *args, **kwargs):
        for field_name, value in request.POST.items():
            # Userモデルにfield_nameというフィールドがあるかチェックする
            if hasattr(request.user, field_name):
                # フィールドがある場合、その値をvalueで上書きする
                setattr(request.user, field_name, value)
        # 上書きしたデータを保存する
        request.user.save()
        return redirect('core:profile_update')


class CreditCardCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'core/credit_card.html')

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY

        try:
            payment_method = stripe.PaymentMethod.create(
                type='card',
                card={
                    'number': request.POST['number'],
                    'exp_month': request.POST['exp_month'],
                    'exp_year': request.POST['exp_year'],
                    'cvc': request.POST['cvc'],
                },
            )

            customer = stripe.Customer.create(
                email=request.user.email,
                payment_method=payment_method
            )
        except stripe.error.CardError as e:
            return JsonResponse({
                'status': 'failed',
                'stripeCode': e.code,
                'message': e.user_message
            })

        User.objects.filter(pk=request.user.pk).update(stripe_customer_id=customer.id)

        return JsonResponse({'status': 'success'})


class AddressUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AddressUpdateForm(instance=request.user)
        return render(request, 'core/address_update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddressUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('core:mypage')
        return render(request, 'core/address_update.html', {'form': form})


class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        User.objects.filter(pk=request.user.pk).update(deleted_at=datetime.now())
        return redirect('core:login')
