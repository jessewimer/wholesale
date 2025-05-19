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

from django.contrib.auth.models import User
from django.db.models import Count

def avail_products_csv(store_num):
    import csv


    store = Store.objects.get(store_number=store_num)
    print(store.name)
    csv_filename = f"{store.name}'s Avail Products.csv"

    avail_products = store.available_products


    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writeheader()

        for item_number, availability in avail_products.items():
            if availability:  # Only write to CSV if the product is available (True)
                writer.writerow([item_number])

    print(f"CSV file '{csv_filename}' has been created with available products.")



def delete_duplicate_stores():

    duplicate_names = Store.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)

    # # Delete duplicate stores except for the one with the lowest primary key
    for name in duplicate_names:
        duplicate_stores = Store.objects.filter(name=name['name']).order_by('pk')

        # Keep the first store (lowest primary key) and delete the rest
        for store in duplicate_stores[1:]:
            store.delete()


    # Retrieve all store objects and print their primary keys
    stores = Store.objects.all()

    for store in stores:
        print(f"Key: {store.pk}: {store.name}")

# resets each store's total orders to 0
def reset_stores():
    stores = Store.objects.all()
    for store in stores:
        store.total_orders = 00
        store.current_order = 00
        store.last_order_date = None
        store.total_num_packets = 0
        store.save()
    print('The following attributes has been zeroed out for all store:')
    print("Total Orders\nCurrent Orders\nLast Order Date\nTotal Number of Pkts")


# Prints a list of all store numbers and names
def view_stores():
    stores = Store.objects.all()
    for store in stores:
        print(store.store_number, " ", store.name)


# Sets all products as 'false' for every store
def set_store_products():
    # Retrieve all store objects
    stores = Store.objects.all()

    # Create a dictionary with item numbers as keys and True as values
    # item_numbers = {num: True for num in range(101, 424)}
    item_numbers = {num: False for num in range(101, 444)}
    for store in stores:
        store.available_products = item_numbers
        store.save()

    print("All products for all stores have been set to false")

# Prints out all store names and available products for each store
def view_stores_products():
    # Retrieve all store objects
    stores = Store.objects.all()

    for store in stores:
        print(store.name, ": ", store.available_products)


def create_store_instance(store_num, username, password, email, name):

    store_number = store_num
    name = name
    email = email

    # Manually set values for the associated User
    username = username
    password = password

    # Create a new User instance
    user = User.objects.create_user(username=username, password=password)

    # Create a new Store instance
    store = Store.objects.create(
        store_number=store_number,
        name=name,
        email=email,
        store_user=user,  # Link the store to the User instance
    )

    # Clear the password from the Store object (if needed)
    store.password = None
    store.save()

    print(f"Store '{name}' has been created successfully.")


def set_store_products_csv(store_num, filename):
    import csv

    store = Store.objects.get(store_number=store_num)
    print(store.name)
    csv_file_path = f"{filename}.csv"

    # Initialize an empty list to store the contents
    true_product_numbers = []

    # Read the CSV file and populate the list
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Assuming the numbers are in the first column of the CSV
            number = int(row[0])
            true_product_numbers.append(number)

        print("length: ", len(true_product_numbers))
        unique_item_numbers_count = len(set(true_product_numbers))
        print("unique item count ", unique_item_numbers_count)
        product_availabilities = {product_number: product_number in true_product_numbers for product_number in range(101, 444)}

        # Assign the product_availabilities dictionary to the store's available_products field
        store.available_products = product_availabilities

        store.save()


def view_store_products(store_num):
    from products.models import Product
    store = Store.objects.get(store_number=store_num)

    available_item_numbers = [item_number for item_number, availability in store.available_products.items() if availability]
    for item in available_item_numbers:
        print(item)

    # matching_products = Product.objects.filter(item_number__in=available_item_numbers)

    # for product in matching_products:
    #     print(f"Veg type: {product.veg_type}, Variety: {product.variety}")


def set_store_slots(store_num, slot_num):
    store = Store.objects.get(store_number=store_num)
    store.slots = slot_num
    store.save()
    print(f"{store.name}'s slots set to {store.slots}")


def update_username(store_num, username):
    store = Store.objects.get(store_number=store_num)

    user = store.store_user
    user.username = username
    user.save()
    print(f"{store.name}'s username has been updated to {username}")

def update_name(store_num, name):
     store = Store.objects.get(store_number=store_num)
     print("before: ", store.name)
     store.name = name
     store.save()
     print("after: ", store.name)


def check_slots(store_num):
    store = Store.objects.get(store_number = store_num)
    print(store.name, " 's slots: ", store.slots)

def add_item_to_store(store_num, item_num):
    store = Store.objects.get(store_number=store_num)

    # Access the available_products dictionary
    available_products = store.available_products

    # Add the new item to the dictionary
    available_products[item_num] = True

    # Assign the modified dictionary back to store.available_products
    store.available_products = available_products

    # Save the changes to the store instance
    store.save()

    print(f"{item_num} has been added to {store.name}'s availabilities")

def add_item_to_stores(store_nums, item_num):
    # Iterate over each store number in the list
    for store_num in store_nums:
        try:
            # Get the store by its store number
            store = Store.objects.get(store_number=store_num)

            # Access the available_products dictionary
            available_products = store.available_products

            # Add the new item to the dictionary
            available_products[item_num] = True

            # Assign the modified dictionary back to store.available_products
            store.available_products = available_products

            # Save the changes to the store instance
            store.save()

            print(f"{item_num} has been added to {store.name}'s availabilities")

        except Store.DoesNotExist:
            print(f"Store with store number {store_num} does not exist.")


def remove_item_from_store(store_num, item_num):
    store = Store.objects.get(store_number=store_num)

    # Access the available_products dictionary
    available_products = store.available_products

    # Add the new item to the dictionary
    available_products[item_num] = False

    # Assign the modified dictionary back to store.available_products
    store.available_products = available_products

    # Save the changes to the store instance
    store.save()

    print(f"{item_num} has been removed {store.name}'s availabilities")

def remove_item_from_all_stores(item_num):
    # Retrieve all store objects
    stores = Store.objects.all()

    for store in stores:
        # Access the available_products dictionary
        available_products = store.available_products

        available_products[item_num] = False

        # Assign the modified dictionary back to store.available_products
        store.available_products = available_products
        print(f'item num {item_num} removed from {store.name}')
        # Save the changes to the store instance
        store.save()
    print(f'Item num {item_num} has been removed from all stores')

def manual_order(store_number, filename):
    # from products.models import Product
    from orders.models import Order
    import csv
    store = Store.objects.get(store_number=store_number)

    # Read data from the CSV file and construct the seed_dict
    seed_dict = {}
    csv_file_path = f"{filename}.csv"
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            product_id = row[0]  # Assuming the first column contains product IDs
            quantity = int(row[1])  # Assuming the second column contains quantities
            seed_dict[product_id] = quantity

    # Call the build_order function with the constructed seed_dict and store object
    order = Order.build_order(seed_dict, store)

    print(f"Store: {order.store}")
    print(f"Order date: {order.order_date}")
    print(f"Total cost: {order.total_cost}")
    print(f"Total packets: {order.total_packets}")
    print(f"Order number: {order.order_number}")
    print(f"Products: {order.products}")





# avail_products_csv(16)
# delete_duplicate stores()
# reset_stores()
# view_stores()
# set_store_products()
# view_stores_products()

# create_store_instance(store_num, username, password, email, name)
# create_store_instance()

# !! to run this function, need to upload a
# csv file to the same directory as the script !!
# set_store_products_csv(52, "peoples")

# remove_item_from_store(store_num, item_num)
# remove_item_from_store(16, 325)

# remove_item_from_all_stores(item_num)
# remove_item_from_all_stores(226)

# view_store_products(15)
set_store_slots(52, 112)
# update_username(52, "anacortes")
# update_name(52, "Ace Hardware - Anacortes")
# check_slots(14)
# add_item_to_store(16, 442)
# add_item_to_stores(store_nums, item_num)
# add_item_to_stores([12, 13, 15, 16, 23, 24, 40, 41, 43, 44, 45, 47, 48, 49], 443)


# manual_order(44, "sno")
