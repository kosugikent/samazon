import stripe

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        stripe.api_key = settings.STRIPE_API_KEY

        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': '4000003920000003',
                'exp_month': 2,
                'exp_year': 2022,
                'cvc': '314',
            },
        )

        stripe.Customer.create(
            email='test@example.com',
            payment_method=payment_method
        )