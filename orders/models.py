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







'''

# models from tkinter/sqlalchemy database

from django.db import models
from products.models import Product
from stores.models import Store
from django.contrib.auth.models import User


class OnlineOrder(models.Model):
    order_number = models.CharField(max_length=100, primary_key=True)
    customer_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField()
    bulk = models.BooleanField(default=False)
    misc = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "online_order"

    def __str__(self):
        return f"OnlineOrder {self.order_number}"


class OOIncludes(models.Model):
    order = models.ForeignKey(OnlineOrder, on_delete=models.CASCADE, related_name="includes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "oo_includes"
        unique_together = ("order", "product")

    def __str__(self):
        return f"{self.qty} × {self.product} in {self.order}"


class OOIncludesMisc(models.Model):
    order = models.ForeignKey(OnlineOrder, on_delete=models.CASCADE, related_name="includes_misc")
    sku = models.CharField(max_length=100)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "oo_includes_misc"
        unique_together = ("order", "sku")

    def __str__(self):
        return f"{self.qty} × {self.sku} in {self.order}"


class PulledOrder(models.Model):
    order_number = models.CharField(max_length=100)

    class Meta:
        db_table = "pulled_order"

    def __str__(self):
        return f"PulledOrder {self.order_number}"


class BatchMetadata(models.Model):
    batch_identifier = models.CharField(max_length=100, unique=True)
    batch_date = models.DateField()
    start_order_number = models.IntegerField()
    end_order_number = models.IntegerField()
    start_order_date = models.DateField()
    end_order_date = models.DateField()

    class Meta:
        db_table = "batch_metadata"

    def __str__(self):
        return f"Batch {self.batch_identifier}"


class BulkBatch(models.Model):
    batch_identifier = models.ForeignKey(BatchMetadata, on_delete=models.CASCADE, related_name="bulk_batches")
    bulk_type = models.CharField(max_length=50)  # 'print' or 'pull'
    sku = models.CharField(max_length=100)
    quantity = models.IntegerField()

    class Meta:
        db_table = "bulk_batch"

    def __str__(self):
        return f"{self.quantity} × {self.sku} in {self.batch_identifier}"


class LastSelected(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="last_selected_order")
    order_number = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "last_selected"

    def __str__(self):
        return f"{self.user.username} last selected {self.order_number or 'None'}"
'''