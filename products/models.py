from django.db import models

class Product(models.Model):
    item_number = models.IntegerField(null=True)
    sku = models.CharField(max_length=11, null=True)
    notes = models.TextField(null=True)
    active = models.CharField(max_length=10, null=True)
    category = models.CharField(max_length=25, null=True)
    super_type = models.CharField(max_length=25, null=True)
    veg_type = models.CharField(max_length=25, null=True)
    sub_type = models.CharField(max_length=25, null=True)
    variety = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True)
    quickbooks_code = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    photo = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.variety

    @classmethod
    def set_price(cls, price):
        for product in cls.objects.all():
            product.set_price(price)

    def print_products(cls):
        for product in cls.objects.all():
            print(f'Item Number: {product.item_number} -- {product.variety}')