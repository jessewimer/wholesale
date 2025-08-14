'''
# models from tkinter/sqlalchemy database 

from django.db import models
from products.models import Variety  # Assuming Variety lives in the products app
from django.utils import timezone


class Grower(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Lot(models.Model):
    variety = models.ForeignKey(Variety, on_delete=models.CASCADE, related_name="lots")
    lot_number = models.CharField(max_length=100)
    grower = models.ForeignKey(Grower, on_delete=models.SET_NULL, null=True, blank=True, related_name="lots")
    year = models.PositiveIntegerField()
    lbs_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lbs_remaining = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    germination_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    test_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_retired = models.BooleanField(default=False)

    class Meta:
        unique_together = ("variety", "lot_number")

    def __str__(self):
        return f"{self.variety} - {self.lot_number}"


class RetiredLot(models.Model):
    lot = models.OneToOneField(Lot, on_delete=models.CASCADE, related_name="retired_info")
    retired_date = models.DateField(default=timezone.now)
    lbs_remaining = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Retired {self.lot}"


class LotNote(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="notes")
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField()

    def __str__(self):
        return f"Note for {self.lot} ({self.created_at:%Y-%m-%d})"
'''