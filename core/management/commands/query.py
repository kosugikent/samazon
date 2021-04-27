from django.core.management import BaseCommand
from django.db.models import F, Avg

from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.\
            values('id').\
            annotate(
                name=F('name'),
                price=F('price'),
                photo=F('photo'),
                star=Avg('reviews__score'),
            ).\
            filter(star__gte=3)
        for p in products:
            print(p)
