from django.db import models
from stores.models import Store
from .models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class Order(models.Model):
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_packets = models.PositiveIntegerField(default=0)
    order_number = models.PositiveIntegerField(default = 0000)     
     
     # dictionary of products/quantities
    products = models.JSONField(default=dict)

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
        self.total
        total = 0
        for product_id, quantity in self.products.items():
            total += get_object_or_404(Product, pk=product_id).price * quantity
        self.total_cost = total * 2.05


    @classmethod
    def build_order(cls, seed_dict, store):
        store.total_orders += 1
        order = self.objects.create()
        order.products = seed_dict
        order.set_order_date()
        order.order_number = store_number + store.total_orders
        order.set_order_totals()
        order.save()
        return order
    
    def calculate_order_packets(self):
        total = 0
        for product_id, quantity in self.products.items():
            total += quantity
        return total

    

    



   
    
    
    # i need a way to get the order date

    # i need a way to get the customer 




    