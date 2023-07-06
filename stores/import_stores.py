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

from stores.models import Store

def import_data():
    csv_file = "C:/Users/ndefe/OneDrive/Desktop/stores.csv"
    encoding = 'utf-8'
    df = pd.read_csv(csv_file, encoding=encoding)  # Read the CSV file using pandas

    for _, row in df.iterrows():
        # Extract the data from each row of the DataFrame
        store_number = row['store_number']
        name = row['name']
        slots = row['slots']
        email = row['email']
        total_pkts = row['total pkts']
        total = row['total $']

        # Create a new Product object and save it to the database
        store = Store(
            store_number=store_number,
            name=name,
            slots=slots,
            email=email,
            total_num_packets=total_pkts,
            total_orders=total
        )
        store.save()

    print("Data import completed.\n\n")

    stores = Store.objects.all()

    print("List of stores:")
    for store in stores:
        print(f"{store.store_number} - {store.name} - {store.slots} - {store.email} - {store.total_num_packets} - {store.total_orders}")

# Call the import_data function
import_data()