import os
import random
from datetime import datetime, timedelta
from django.utils import timezone

from django_optimization_tips.settings import BASE_DIR
from products.models import Variation, Product, Sale, Measurement

NUMBER_OF_PRODUCTS = 1000
NUMBER_OF_SALES_PER_PRODUCT = 100

BRANDS = [
    'Nike', 'Adidas', 'Reebok', 'Timberland', 'Versace', 'Swatch', 'Swarovski',
    'Ray-Ban', 'Pepe Jeans', 'Oakley', 'Lacoste', 'Hugo Boss', 'Ferrari',
    'Diesel', 'Casio', 'Armani', 'Adolfo Dominguez'
]


def create_variations():
    size_variations = [
        Variation.objects.create(variation_type="Size", variation_value="XS"),
        Variation.objects.create(variation_type="Size", variation_value="S"),
        Variation.objects.create(variation_type="Size", variation_value="M"),
        Variation.objects.create(variation_type="Size", variation_value="L"),
        Variation.objects.create(variation_type="Size", variation_value="XL"),
        Variation.objects.create(variation_type="Size", variation_value="XXL")
    ]
    color_variations = [
        Variation.objects.create(
            variation_type="Color", variation_value="Red"
        ),
        Variation.objects.create(
            variation_type="Color", variation_value="White"
        ),
        Variation.objects.create(
            variation_type="Color", variation_value="Black"
        ),
        Variation.objects.create(
            variation_type="Color", variation_value="Yellow"
        ),
        Variation.objects.create(
            variation_type="Color", variation_value="Orange"
        ),
        Variation.objects.create(
            variation_type="Color", variation_value="Green"
        ),
    ]
    return size_variations, color_variations


def create_string(words, maximun_number_of_words):
    number_of_words = random.randint(0, maximun_number_of_words - 1)
    name = words[random.randint(0, len(words))]
    for _ in range(number_of_words):
        name += ' ' + words[random.randint(0, len(words) - 1)]
    return name


def create_products(size_variations, color_variations):
    word_file = os.path.join(BASE_DIR, "utils", "words.txt")
    words = open(word_file).read().splitlines()

    yesterday = timezone.now() - timedelta(days=1)
    first_day = yesterday - timedelta(days=NUMBER_OF_SALES_PER_PRODUCT - 1)

    sales = []
    for product_index in range(NUMBER_OF_PRODUCTS):
        current_price = round(random.uniform(5, 100), 2)
        cost = round(
            current_price - (current_price * random.uniform(0.3, 0.5)), 2
        )
        minimum_price_allowed = round(
            current_price - (current_price * random.uniform(0.1, 0.3)), 2
        )
        maximum_price_allowed = round(
            current_price + (current_price * random.uniform(0.1, 0.3)), 2
        )
        product = Product.objects.create(
            sku=str(product_index + 1000), name=create_string(words, 3),
            part_number=str(product_index), description=create_string(words, 20),
            brand=BRANDS[random.randint(0, len(BRANDS) - 1)],
            category_level_1=create_string(words, 2),
            category_level_2=create_string(words, 2),
            category_level_3=create_string(words, 2),
            category_level_4=create_string(words, 2),
            category_level_5=create_string(words, 2),
            ean=str(product_index + 1000), current_price=current_price,
            cost=cost, stock=random.randint(10, 150),
            weight=round(random.uniform(1, 10), 2),
            shipping_cost=round(random.uniform(1, 10), 2),
            minimum_price_allowed=minimum_price_allowed,
            maximum_price_allowed=maximum_price_allowed,
            active=True
        )

        variations = []
        for size_variation in size_variations:
            if random.randint(0, 10) > 2:
                variations.append(size_variation)
        for color_variation in color_variations:
            if random.randint(0, 10) > 5:
                variations.append(color_variation)
        product.product_variations.add(*variations)
        product.save()

        current_date = first_day

        while current_date <= yesterday:
            sales.append(Sale(
                product=product,
                date=current_date,
                quantity_purchased=random.randint(1, 10),
                price=current_price,
                discount=round(random.uniform(0, 15), 2),
                vat=random.randint(0, 21),
            ))
            current_date = current_date + timedelta(days=1)
    Sale.objects.bulk_create(sales)


def clean_database():
    Measurement.objects.all().delete()
    Variation.objects.all().delete()
    Product.objects.all().delete()
    Sale.objects.all().delete()


def load_database():
    clean_database()
    size_variations, color_variations = create_variations()
    create_products(size_variations, color_variations)
