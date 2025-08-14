from django.db import models

'''

class OfficeSupply(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    item_num = models.CharField(max_length=100, blank=True, null=True)
    vendor = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "office_supplies"

    def __str__(self):
        return f"{self.item} ({self.item_num})"

        '''