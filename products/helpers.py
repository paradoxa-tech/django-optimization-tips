import datetime

from django.db.models import Sum, Q

from products.models import Product, Sale, IntermediateProduct


class ProcessTableData:

    def __init__(self, page_length, start, order_column, order_dir, search):
        self.page_length = page_length
        self.start = start
        self.order_column = order_column
        self.order_dir = order_dir
        self.search = search

        self.data = self.task_2_generate_data()

    # def task_5_sort_data(self, product_queryset):
    def task_5_sort_data(self, products_queryset):
        headers_index = {
            "0": "sku",
            "1": "name",
            "2": "brand",
            "3": "category_level_1",
            "5": "price",
            "6": "profit",
            "7": "last_month_sales"
        }
        column = headers_index[self.order_column]
        if self.order_dir == "asc":
            column = '-' + column
        return products_queryset.order_by(column)

    # self.task_4_search_data(product_queryset):
    def task_4_search_data(self, products_queryset):
        if not self.search:
            return products_queryset

        return products_queryset.filter(
            Q(sku__icontains=self.search) |
            Q(name__icontains=self.search) |
            Q(brand__icontains=self.search) |
            Q(category_level_1__icontains=self.search)
        )

    def calculate_total_records(self):
        return len(self.data)

    def get_data(self):
        return self.data

    def task_2_generate_data(self):
        table_info = []
        products = IntermediateProduct.objects.all()

        products = self.task_4_search_data(products)
        sorted_products = self.task_5_sort_data(products)

        for product in sorted_products:
            product_info = dict()
            product_info["sku"] = product.sku
            product_info["name"] = product.name
            product_info["variations"] = product.variations
            product_info["brand"] = product.brand
            product_info["category_level_1"] = product.category_level_1
            product_info["profit"] = product.profit
            product_info["price"] = product.price
            product_info["last_month_sales"] = product.last_month_sales

            table_info.append(product_info)

        return table_info

    @staticmethod
    def get_product_variations(product):
        variations = product.product_variations.all()
        return [
            f" {v.variation_type}: {v.variation_value}" for v in variations
        ]

    @staticmethod
    def get_product_profit(product):
        profit = product.current_price - product.cost
        return profit

    @staticmethod
    def task_3_get_last_month_sales(product):
        today = datetime.date.today()
        last_month_date = today - datetime.timedelta(days=30)
        last_month_sales = Sale.objects.filter(
            product=product, date__gte=last_month_date
        ).aggregate(
            Sum('quantity_purchased')
        )['quantity_purchased__sum']

        if not last_month_sales:
            return 0
        return last_month_sales


def update_intermediate_products():
    intermediate_products = []
    products = Product.objects.filter().prefetch_related("product_variations")

    for product in products:
        intermediate_product = IntermediateProduct()
        intermediate_product.product = product
        intermediate_product.sku = product.sku
        intermediate_product.name = product.name
        intermediate_product.brand = product.brand
        intermediate_product.category_level_1 = product.category_level_1
        intermediate_product.price = product.current_price
        intermediate_product.variations = \
            ProcessTableData.get_product_variations(product)
        intermediate_product.profit = \
            ProcessTableData.get_product_profit(product)
        intermediate_product.last_month_sales = \
            ProcessTableData.task_3_get_last_month_sales(product)

        intermediate_products.append(intermediate_product)

    IntermediateProduct.objects.all().delete()
    IntermediateProduct.objects.bulk_create(intermediate_products)
