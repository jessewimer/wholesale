from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.db import models

class Store(models.Model):
    store_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    store_number = models.IntegerField(null=True)
    password = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    slots = models.IntegerField(null=True)
    last_order_date = models.DateField(null=True, blank=True)
    total_orders = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_num_packets = models.IntegerField(default=0)
    available_products = models.JSONField(default=dict)

    def add_available_product(self, product_id):
        self.available_products[str(product_id)] = True

    def remove_available_product(self, product_id):
        del self.available_products[str(product_id)]

    def is_product_available(self, product_id):
        return self.available_products.get(str(product_id), False)

    def get_orders(self):
        return self.order_set.all()

    # need to add various functions below to give stores functionality    
    def add_order(self, order_amount):
        self.current_order = order_amount
        self.total_orders += order_amount
        self.last_order_date = timezone.now().date()
        self.save()

    # def reset_total_orders(self):
    #     self.total_orders = 0
    #     self.save()

    def __str__(self):
        return self.name

    def print_store_ids():
        stores = Store.objects.order_by('id')
        for store in stores:
            print(f"Key: {store.id}, Name: {store.name}")