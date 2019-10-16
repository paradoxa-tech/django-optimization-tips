import datetime

from products.models import Product, Sale


class ProcessTableData:

    def __init__(self, page_length, start, order_column, order_dir, search):
        self.page_length = page_length
        self.start = start
        self.order_column = order_column
        self.order_dir = order_dir
        self.search = search

        self.data = self.generate_data()

    def sort_data(self):
        headers_index = {
            "0": "sku",
            "1": "name",
            "2": "brand",
            "3": "category_level_1",
            "4": "variations",
            "5": "price",
            "6": "margin",
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

    def search_data(self):
        search_data = []
        for row in self.data:
            search = self.search.lower()
            if search in row["sku"].lower() \
                    or search in row["name"].lower() \
                    or search in row["branc"].lower() \
                    or search in row["category_level_1"].lower() \
                    or search in row["variations"].lower()
                search_data.append(row)
        self.data = search_data

    def calculate_total_records(self):
        return len(self.data)

    def get_data(self):
        return self.data

    def generate_data(self):
        table_info = []
        products_ids = Product.objects.filter().values_list('id', flat=True)
        for product_id in products_ids:
            product = Product.objects.get(id=product_id)
            product_info = dict()
            product_info["sku"] = product.sku
            product_info["name"] = product.name
            product_info["variations"] = self.get_product_variations(product)
            product_info["brand"] = product.brand
            product_info["category_level_1"] = product.category_level_1
            product_info["margin"] = self.get_product_margin(product)
            product_info["price"] = product.current_price
            product_info["last_month_sales"] = self.get_last_month_sales(
                product
            )

            table_info.append(product_info)

        return table_info

    @staticmethod
    def get_product_variations(product):
        return product.product_variations.values()

    @staticmethod
    def get_product_margin(product):
        margin = product.current_price - product.cost
        return margin

    @staticmethod
    def get_last_month_sales(product):
        sales = Sale.objects.filter(product=product)
        today = datetime.date.today()
        last_month_date = today - datetime.timedelta(days=30)
        quantity_acc = 0
        for sale in sales:
            if sale.date <= last_month_date:
                quantity_acc += sale.quantity_purchased

        return quantity_acc
