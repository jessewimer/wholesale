# Generated by Django 4.1.2 on 2023-09-05 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="variety",
            field=models.CharField(max_length=30, null=True),
        ),
    ]