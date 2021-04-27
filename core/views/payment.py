import stripe

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import View

from core.models import Order, PurchaseHistory


class PaymentView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_API_KEY

        try:
            payment_intent = stripe.PaymentIntent.create(
                customer=request.user.stripe_customer_id,
                amount=request.POST['amount'],
                currency='jpy',
                payment_method_types=['card'],
            )

            payment_methods = stripe.PaymentMethod.list(
                customer=request.user.stripe_customer_id,
                type='card',
            )

            payment_method = payment_methods['data'][0]['id']

            response = stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method=payment_method,
            )
        except stripe.error.CardError as e:
            return JsonResponse({
                'status': 'failed',
                'stripeCode': e.code,
                'message': e.user_message
            })

        order = Order.objects.create(
            payment_intent_id=response.id,
            user=request.user,
            total_amount=request.POST['amount'],
        )

        for cart in request.user.carts.all():
            PurchaseHistory.objects.create(
                order=order,
                product=cart.product,
                qty=cart.qty,
                amount=cart.sum(),
            )

        request.user.carts.all().delete()

        return JsonResponse({'status': 'succeeded'})
