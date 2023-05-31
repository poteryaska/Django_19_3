from django.core.management import BaseCommand

from main.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        product_list = [
            {'name': 'apple', 'price': 130, 'category': 'fruits'},
            {'name': 'cucumber', 'price': 120, 'category': 'vegetables'},
            {'name': 'chicken', 'price': 100, 'category': 'meat'},
            {'name': 'fish', 'price': 700, 'category': 'seafood'},
        ]

        old_products = []
        product_for_create = []
        for product in product_list:
            # if product['name'] !=
            product_for_create.append(
                Product(**product)
            )

        Product.objects.bulk_create(product_for_create)