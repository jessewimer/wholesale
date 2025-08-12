from django.db import models
from stores.models import Store
from products.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    # order_date = models.DateField(auto_now_add=True)
    order_date = models.DateField()
    order_number = models.CharField(max_length=20, unique=True)
    pulled_for_processing = models.BooleanField(default=False)
    pulled_at = models.DateTimeField(null=True, blank=True)

    products = models.ManyToManyField(Product, through='OrderIncludes')

    def __str__(self):
        return f"{self.store.name} -- Order #{self.order_number}"

    def add_product(self, product_id, quantity):
        product = get_object_or_404(Product, pk=product_id)
        include, created = OrderIncludes.objects.get_or_create(order=self, product=product)

        if not created:
            include.quantity += quantity
        else:
            include.quantity = quantity

        include.save()
        self.set_order_totals()

    def set_order_date(self):
        self.order_date = timezone.now().date()
        self.save()

    def set_order_totals(self):
        total_packets = 0
        total_cost = 0

        for include in OrderIncludes.objects.filter(order=self):
            total_packets += include.quantity
            total_cost += include.quantity * include.product.price

        self.total_packets = total_packets
        self.total_cost = total_cost
        self.save()
        return total_packets

    @classmethod
    def build_order(cls, seed_dict, store):
        current_year = timezone.now().year % 100  # e.g., 2026 -> 26

        # Count how many orders this store has made this year
        this_year_orders = cls.objects.filter(
            store=store,
            order_date__year=timezone.now().year
        ).count() + 1

        order_number = f"W{store.store_number:02d}{this_year_orders:02d}-{current_year:02d}"

        order = cls.objects.create(store=store, order_number=order_number)
        order.set_order_date()

        for product_id, quantity in seed_dict.items():
            order.add_product(product_id, quantity)

        store.total_orders += 1
        store.total_num_packets = order.total_packets
        store.save()

        return order

    def calculate_order_packets(self):
        return OrderIncludes.objects.filter(order=self).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0


class OrderIncludes(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"Order #{self.order.order_number} - {self.product.name} x {self.quantity}"
