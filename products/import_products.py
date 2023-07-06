import pandas as pd
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

def import_data():
    csv_file = "C:/Users/ndefe/OneDrive/Desktop/products.csv"
    encoding = 'utf-8'
    df = pd.read_csv(csv_file, encoding=encoding)  # Read the CSV file using pandas

    for _, row in df.iterrows():
        # Extract the data from each row of the DataFrame
        item_number = row['item number']
        sku = row['sku']
        notes = row['notes']
        active = row['active']
        category = row['category']
        super_type = row['supertype']
        veg_type = row['type']
        sub_type = row['subtype']
        variety = row['variety']
        description = row['description']
        quickbooks_code = row['qb code']
    
        # Create a new Product object and save it to the database
        product = Product(
            item_number=item_number,
            sku=sku,
            active=active,
            category=category,
            super_type=super_type,
            veg_type=veg_type,
            sub_type=sub_type,
            variety=variety,
            description=description,
            quickbooks_code=quickbooks_code
        )
        product.save()

    print("Data import completed.")

# Call the import_data function
import_data()
