import datetime

from django.db.models import Sum, Q

from products.models import Product, Sale


class ProcessTableData:

    def __init__(self, page_length, start, order_column, order_dir, search):
        self.page_length = page_length
        self.start = start
        self.order_column = order_column
        self.order_dir = order_dir
        self.search = search

        self.data = self.task_2_generate_data()

    # def task_5_sort_data(self, product_queryset):
    def task_5_sort_data(self):
        headers_index = {
            "0": "sku",
            "1": "name",
            "2": "brand",
            "3": "category_level_1",
            "5": "price",
            "6": "profit",
            "7": "last_month_sales"
        }

        if self.order_dir == "asc":
            reverse = False
        else:
            reverse = True

        self.data = sorted(
            self.data,
            key=lambda i: i[headers_index[self.order_column]],
            reverse=reverse
        )

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
        products = Product.objects.all().only(
            'sku', 'name', 'product_variations', 'brand',
            'category_level_1', 'current_price', 'cost'
        ).prefetch_related('product_variations')

        products = self.task_4_search_data(products)

        for product in products:
            product_info = dict()

            product_info["sku"] = product.sku
            product_info["name"] = product.name
            product_info["variations"] = self.get_product_variations(product)
            product_info["brand"] = product.brand
            product_info["category_level_1"] = product.category_level_1
            product_info["profit"] = self.get_product_profit(product)
            product_info["price"] = product.current_price
            product_info["last_month_sales"] = self.task_3_get_last_month_sales(
                product
            )

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
        return Sale.objects.filter(
            product=product, date__gte=last_month_date
        ).aggregate(
            Sum('quantity_purchased')
        )['quantity_purchased__sum']
