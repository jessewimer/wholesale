import os
import django
import sys
import csv
from prettytable import PrettyTable
# Get the current directory path
current_path = os.path.dirname(os.path.abspath(__file__))

# Get the project directory path by going up two levels from the current directory
project_path = os.path.abspath(os.path.join(current_path, '..'))

# Add the project directory to the sys.path
sys.path.append(project_path)

# Set the DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wholesale.settings")
django.setup()

from stores.models import Store, StoreProduct
from products.models import Product
from django.contrib.auth.models import User
from django.db.models import Count
from django.db import connection


# Sets all storeproduct entries as 'false' so all store have no product available
def reset_storeproduct_table():
    # Delete all StoreProduct records
    StoreProduct.objects.all().delete()
    print("Deleted all StoreProduct records.")

    # Reset auto-increment for MySQL
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE stores_storeproduct AUTO_INCREMENT = 1;")
    print("Reset StoreProduct AUTO_INCREMENT.")

    # Then create all combinations like before
    stores = Store.objects.all()
    products = Product.objects.all()

    to_create = []
    for store in stores:
        for product in products:
            to_create.append(StoreProduct(store=store, product=product, is_available=False))

    StoreProduct.objects.bulk_create(to_create)
    print(f"Created {len(to_create)} StoreProduct entries with is_available=False.")


def print_storeproduct_table():

    # Create table with headers
    table = PrettyTable()
    table.field_names = ["Store Number", "Store Name", "Product Item #", "Product Name", "Available"]

    # Query all StoreProduct entries with related store and product
    storeproducts = StoreProduct.objects.select_related('store', 'product').order_by('store__store_number', 'product__item_number')

    for sp in storeproducts:
        table.add_row([
            sp.store.store_number,
            sp.store.name,
            sp.product.item_number,
            str(sp.product),
            "Yes" if sp.is_available else "No"
        ])

    print(table)


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


# Prints a list of all store numbers and names
def view_stores():
    stores = Store.objects.all()
    for store in stores:
        print(store.store_number, " ", store.name)


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


def set_items_availability(store_nums, item_nums=None, availability=True, csv_filename=None):
    # Normalize store_nums to list
    if isinstance(store_nums, int):
        store_nums = [store_nums]

    # Load item_nums from CSV if filename given
    if csv_filename:
        csv_path = os.path.join(os.path.dirname(__file__), 'csv', csv_filename)
        try:
            with open(csv_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                item_nums = []
                for row in reader:
                    for val in row:
                        try:
                            item_nums.append(int(val.strip()))
                        except ValueError:
                            print(f"Skipping non-integer value in CSV: {val}")
            print(f"Loaded {len(item_nums)} total item numbers from {csv_filename}")
            print(f"Unique item numbers loaded: {len(set(item_nums))}")
        except FileNotFoundError:
            print(f"CSV file not found: {csv_path}")
            return
    else:
        # Normalize item_nums to list if given directly
        if isinstance(item_nums, int):
            item_nums = [item_nums]
        if item_nums is None:
            print("No item_nums provided and no csv_filename given.")
            return

    # Validate availability is a boolean
    if not isinstance(availability, bool):
        raise ValueError("Availability parameter must be True or False")

    # Query stores
    stores = Store.objects.filter(store_number__in=store_nums)
    found_store_nums = set(stores.values_list('store_number', flat=True))
    missing_stores = set(store_nums) - found_store_nums
    for ms in missing_stores:
        print(f"Store with store_number={ms} does not exist.")
    print(f"Found {stores.count()} stores matching input.")

    # Query products
    products = Product.objects.filter(item_number__in=item_nums)
    print(f"Product queryset count matching item_nums: {products.count()}")

    # Show any missing products from item_nums not in DB
    product_item_numbers = set(products.values_list('item_number', flat=True))
    missing_products = set(item_nums) - product_item_numbers
    if missing_products:
        print(f"Warning: {len(missing_products)} item_numbers not found in Products DB: {sorted(missing_products)}")

    # Check how many StoreProduct rows will be affected
    matching_storeproducts = StoreProduct.objects.filter(store__in=stores, product__in=products)
    print(f"StoreProduct records matching filter before update: {matching_storeproducts.count()}")

    # Perform update
    updated_count = matching_storeproducts.update(is_available=availability)
    print(f"Updated {updated_count} StoreProduct records to is_available={availability}.")

    # Print updated stores info
    for store in stores:
        print(f"Updated products for store: {store.name}")



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




# reset_storeproduct_table()
# print_storeproduct_table()



# def set_items_availability(store_nums, item_nums=None, availability=True, csv_filename=None):
set_items_availability(43, list(range(101,401)), True)
# set_items_availability([52], availability=True, csv_filename='walts.csv')

# avail_products_csv(16)
# delete_duplicate stores()

# view_stores()
# set_store_products()


# create_store_instance(store_num, username, password, email, name)
# create_store_instance()

# !! to run this function, need to upload a
# csv file to the same directory as the script !!
# set_store_products_csv(52, "peoples")

# remove_item_from_all_stores(item_num)
# remove_item_from_all_stores(226)

# view_store_products(15)
# set_store_slots(52, 112)
# check_slots(14)
# update_username(52, "anacortes")
# update_name(52, "Ace Hardware - Anacortes")





# manual_order(44, "sno")
