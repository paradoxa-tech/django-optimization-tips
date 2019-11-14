from django.db import models


class Measurement(models.Model):
    request_time = models.FloatField(blank=True, null=True)
    number_of_queries = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(
        auto_created=True, auto_now_add=True, blank=True, null=True
    )


class Variation(models.Model):
    variation_type = models.CharField(max_length=1000, blank=True, null=True)
    variation_value = models.CharField(max_length=1000, blank=True, null=True)


class Product(models.Model):
    sku = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    part_number = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=1000, blank=True, null=True)
    category_level_1 = models.CharField(max_length=1000, blank=True, null=True)
    category_level_2 = models.CharField(max_length=1000, blank=True, null=True)
    category_level_3 = models.CharField(max_length=1000, blank=True, null=True)
    category_level_4 = models.CharField(max_length=1000, blank=True, null=True)
    category_level_5 = models.CharField(max_length=1000, blank=True, null=True)
    ean = models.CharField(max_length=1000, blank=True, null=True)
    current_price = models.DecimalField(
        max_digits=20, decimal_places=5, blank=True, null=True
    )
    current_discount = models.DecimalField(
        max_digits=20, decimal_places=5, default=0, blank=True, null=True
    )
    cost = models.DecimalField(
        max_digits=20, decimal_places=5, default=0, blank=True, null=True
    )
    stock = models.IntegerField(default=0, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    shipping_cost = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True, null=True
    )
    minimum_price_allowed = models.FloatField(blank=True, null=True)
    maximum_price_allowed = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=True)
    product_variations = models.ManyToManyField(Variation)
    created_at = models.DateTimeField(
        auto_created=True, auto_now_add=True, blank=True, null=True
    )


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField()
    quantity_purchased = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    vat = models.PositiveSmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class IntermediateProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    brand = models.CharField(max_length=1000, blank=True, null=True)
    category_level_1 = models.CharField(max_length=1000, blank=True, null=True)
    variations = models.CharField(max_length=1000, blank=True, null=True)
    price = models.FloatField()
    profit = models.FloatField()
    last_month_sales = models.IntegerField()
