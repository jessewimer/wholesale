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

    print("List of Varieties:")
    for variety in varieties:
        print(variety)

# Call the function to print the list of varieties
print_varieties()

