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

def print_varieties():
    varieties = Product.objects.values_list('variety', flat=True).distinct()
    primary_keys = Product.objects.values_list('pk', flat=True).distinct()
    i = 0
    print("List of Varieties:")
    for variety in varieties:
        print(primary_keys[i], variety)
        i += 1

# Function to print the list of varieties and their various attributes
def print_database():
    products = Product.objects.all()
    for product in products:
        # Can set the price of the product here
        #product.price = 2.05
        
        # if product.sub_type == "nan":
        #     product.sub_type = ""
        # product.save()
        print(product.item_number, product.variety)
        
        # print(product.pk, product.variety, product.sub_type, product.price, product.photo)    

#print_varieties()
print_database()

