from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
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
    # total_orders = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # current_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # total_num_packets = models.IntegerField(default=0)
    available_products = models.ManyToManyField(
        'products.Product',
        through='StoreProduct',
        related_name='available_in_stores'
    )

    def __str__(self):
        return self.name

class StoreProduct(models.Model):
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)

    class Meta:
        unique_together = ('store', 'product')



'''
# models from tkinter/sqlalchemy database

from django.db import models
from products.models import Product  # assuming Product is in the products app
from django.contrib.auth.models import User


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    store_contact_name = models.CharField(max_length=255, blank=True, null=True)
    store_contact_phone = models.CharField(max_length=50, blank=True, null=True)
    store_contact_email = models.EmailField(blank=True, null=True)
    store_address = models.TextField(blank=True, null=True)
    store_city = models.CharField(max_length=255, blank=True, null=True)
    store_state = models.CharField(max_length=255, blank=True, null=True)
    store_zip = models.CharField(max_length=20, blank=True, null=True)
    store_country = models.CharField(max_length=255, blank=True, null=True)
    store_notes = models.TextField(blank=True, null=True)
    store_created = models.DateTimeField(auto_now_add=True)
    store_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "store"

    def __str__(self):
        return self.store_name


class StoreNote(models.Model):
    note_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "store_note"

    def __str__(self):
        return f"Note for {self.store.store_name} ({self.created_at:%Y-%m-%d})"


class StoreOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField()
    fulfilled_date = models.DateTimeField(blank=True, null=True)
    is_fulfilled = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "store_order"

    def __str__(self):
        return f"Order {self.order_id} for {self.store.store_name}"


class SOIncludes(models.Model):
    soi_id = models.AutoField(primary_key=True)
    store_order = models.ForeignKey(StoreOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price_each = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "so_includes"

    def __str__(self):
        return f"{self.quantity} × {self.product} in Order {self.store_order_id}"


class LastSelectedStore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="last_selected_store")
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "last_selected_store"

    def __str__(self):
        return f"{self.user.username} last selected {self.store.store_name if self.store else 'None'}"

'''