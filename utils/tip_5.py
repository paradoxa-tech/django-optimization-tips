from django.db import connection
from products.models import Product


def looping():
    initial_number_of_queries = len(connection.queries)
    products = Product.objects.filter(id__lte=5)
    products_with_low_id = {}
    for id_ in range(1, 5):
        try:
            products_with_low_id[id_] = products.get(id=id_)  # Database query on each iteration
        except Product.DoesNotExist:
            pass

    print(f"First result: {products_with_low_id}")
    print(f"Number of queries first attempt: {len(connection.queries) - initial_number_of_queries}")

    # DO
    initial_number_of_queries = len(connection.queries)
    products = Product.objects.filter(id__lte=5)
    products_with_low_id = {}
    lookup = {product.id: product for product in products}  # Evaluate the QuerySet and construct lookup
    for id_ in range(1, 5):
        try:
            products_with_low_id[id_] = lookup[id_]  # No database query
        except KeyError:
            pass
    print(f"Second result: {products_with_low_id}")
    print(f"Number of queries second attempt: {len(connection.queries) - initial_number_of_queries}")
