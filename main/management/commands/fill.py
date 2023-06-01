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


        product_for_create = []




        for product in product_list:
            if product['name'] not in old_products:
                product_for_create.append(
                    Product(**product)
                )
            # elif product['name'] in old_products:

        Product.objects.update_or_create(product_for_create)