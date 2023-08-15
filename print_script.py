import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wholesale.settings')

# Initialize Django
django.setup()

# Import the Store model
from django.db.models import Count
from stores.models import Store

# duplicate_names = Store.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)

# # Delete duplicate stores except for the one with the lowest primary key
# for name in duplicate_names:
#     duplicate_stores = Store.objects.filter(name=name['name']).order_by('pk')

#     # Keep the first store (lowest primary key) and delete the rest
#     for store in duplicate_stores[1:]:
#         store.delete()


# Retrieve all store objects and print their primary keys
stores = Store.objects.all()

for store in stores:
    #print(f"Key: {store.pk}: {store.name} {store.email}")
    print(f"Key: {store.pk}: {store.name} {store.email}")
