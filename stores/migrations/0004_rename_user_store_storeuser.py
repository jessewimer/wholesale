# Generated by Django 4.1.2 on 2023-07-30 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stores", "0003_storeuser"),
    ]

    operations = [
        migrations.RenameField(
            model_name="store",
            old_name="user",
            new_name="storeuser",
        ),
    ]
