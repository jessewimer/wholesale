#import pandas as pd
from django.core.files.storage import default_storage
from django.conf import settings
import os
import django
import sys

# Get the current directory path
current_path = os.path.dirname(os.path.abspath(__file__))

# Get the project directory path by going up two levels from the current directory
project_path = os.path.abspath(os.path.join(current_path, '..'))

# Add the project directory to the sys.path
sys.path.append(project_path)

# Set the DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wholesale.settings")
django.setup()

from products.models import Product

def update_product_photos():
    products = Product.objects.all()

    for product in products:
        item_number = str(product.item_number)
        webp_path = os.path.join('products', 'photos', f'{item_number}.webp')
        jpg_path = os.path.join('products', 'photos', f'{item_number}.jpg')

        # Check if the WebP image exists and set the photo attribute accordingly
        if product_has_image(webp_path):
            print('webp image')
            product.photo = f'{webp_path}'
        elif product_has_image(jpg_path):
            print('jpg image')
            product.photo = f'{jpg_path}'
        else:
            # If neither WebP nor JPG image exists, set it to a default image
            print('default image')
            product.photo = f'products/photos/default.jpg'
        
        product.save()

def product_has_image(image_path):
    # Use os.path.join to construct the absolute image path within STATIC_ROOT
    full_image_path = os.path.join(settings.STATIC_ROOT, image_path)
    return os.path.exists(full_image_path)

# Call the function to update the photos for all products
update_product_photos()

print("photos set successfully")