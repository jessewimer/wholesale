# Generated by Django 4.1.2 on 2023-09-05 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("item_number", models.IntegerField(null=True)),
                ("sku", models.CharField(max_length=11, null=True)),
                ("notes", models.TextField(null=True)),
                ("active", models.CharField(max_length=10, null=True)),
                ("category", models.CharField(max_length=25, null=True)),
                ("super_type", models.CharField(max_length=25, null=True)),
                ("veg_type", models.CharField(max_length=25, null=True)),
                ("sub_type", models.CharField(max_length=25, null=True)),
                ("variety", models.CharField(max_length=25, null=True)),
                ("description", models.TextField(null=True)),
                ("quickbooks_code", models.CharField(max_length=50, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                ("photo", models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
