# Generated by Django 4.1.2 on 2023-06-29 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_product_item_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="active",
            field=models.CharField(max_length=10, null=True),
        ),
    ]
