# Generated by Django 2.2.6 on 2019-10-15 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, null=True)),
                ('sku', models.CharField(blank=True, max_length=1000, null=True)),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('part_number', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, max_length=2000, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('brand', models.CharField(blank=True, max_length=1000, null=True)),
                ('category_level_1', models.CharField(blank=True, max_length=1000, null=True)),
                ('category_level_2', models.CharField(blank=True, max_length=1000, null=True)),
                ('category_level_3', models.CharField(blank=True, max_length=1000, null=True)),
                ('category_level_4', models.CharField(blank=True, max_length=1000, null=True)),
                ('category_level_5', models.CharField(blank=True, max_length=1000, null=True)),
                ('ean', models.CharField(blank=True, max_length=1000, null=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('current_discount', models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=20, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=20, null=True)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('shipping_cost', models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True)),
                ('minimum_price_allowed', models.FloatField(blank=True, null=True)),
                ('maximum_price_allowed', models.FloatField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_type', models.CharField(blank=True, max_length=1000, null=True)),
                ('variation_value', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('date', models.DateTimeField()),
                ('quantity_purchased', models.PositiveIntegerField(default=0)),
                ('price', models.FloatField()),
                ('discount', models.FloatField(blank=True, null=True)),
                ('vat', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_variations',
            field=models.ManyToManyField(to='products.Variation'),
        ),
    ]
