from django.db import models
from stores.models import Store
from products.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    order_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_packets = models.PositiveIntegerField(default=0)
    order_number = models.PositiveIntegerField(default=0000)     
    products = models.JSONField(default=dict) # dictionary of products/quantities

    def __str__(self):
        return f"{self.store.name} -- Order #{self.store.order_number}"
    
    def add_product(self, product_id, quantity):
        self.products[str(product_id)] = quantity
        self.total_packets += quantity
        self.total_cost += get_object_or_404(Product, pk=product_id).price * quantity
        self.save()

    def set_order_date(self):
        self.order_date = timezone.now().date()
        self.save()

    def set_order_totals(self):
        total = 0
        for product_id, quantity in self.products.items():
            total += quantity
        self.total_packets = total
        self.total_cost = self.total_packets * 2.05
        self.save()
        return total

    #order_number not getting set properly
    @classmethod
    def build_order(cls, seed_dict, store):
        store.total_orders += 1
        order = cls.objects.create()
        order.store = store
        order.products = seed_dict
        order.set_order_date()
 
        order.order_number = int(f"{store.store_number}{int(store.total_orders):02d}")
   
        store.total_num_packets = order.set_order_totals()

        order.save()
        store.save()
        return order
    
    def calculate_order_packets(self):
        total = 0
        for product_id, quantity in self.products.items():
            total += quantity
        return total    