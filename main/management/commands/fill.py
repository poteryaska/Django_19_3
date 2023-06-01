from django.core.management import BaseCommand

from main.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):

        product_list = [
            {'name': 'apple', 'price': 130, 'category': 'fruits'},
            {'name': 'cucumber', 'price': 120, 'category': 'vegetables'},
            {'name': 'chicken', 'price': 100, 'category': 'meat'},
            {'name': 'mussels', 'price': 700, 'category': 'seafood'},
        ]

        product_for_create = []

        if Product.objects.all() is not None:
            Product.objects.all().delete()
            for product in product_list:
                product_for_create.append(
                    Product(**product)
                )
            Product.objects.bulk_create(product_for_create)
        else:
            Product.objects.bulk_create(product_for_create)
