from django.conf import settings
import os
import django
import sys
import csv
from prettytable import PrettyTable
from collections import Counter
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

def print_product_table():
    products = Product.objects.all().order_by('item_number').values('item_number', 'sku', 'variety')

    table = PrettyTable()
    table.field_names = ["Item Number", "SKU", "Variety"]

    for p in products:
        table.add_row([p['item_number'], p['sku'], p['variety']])

    print(table)


def check_duplicate_item_numbers():
    # Get all item_numbers from products
    item_numbers = Product.objects.values_list('item_number', flat=True)

    # Count occurrences of each item_number
    counts = Counter(item_numbers)

    # Find duplicates
    duplicates = {num: count for num, count in counts.items() if count > 1}

    if duplicates:
        print("Duplicate item_numbers found:")
        for item_num, count in duplicates.items():
            print(f"Item Number: {item_num} - Count: {count}")
    else:
        print("No duplicate item_numbers found.")


def update_notes_with_csv():

    with open('notes.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            item_num = row[0]
            note = row[1]
            product = Product.objects.get(item_number=item_num)

            if note == "B":
                product.notes = "Best Seller"
            elif note == "NR":
                product.notes = "New/Returning"
            elif note == "L":
                product.notes = "Limited Availability"
            else:
                product.notes = "-"

            product.save()
            print(f"{product.item_number} -- {product.notes}")


def check_categories():
    products = Product.objects.all()
    for product in products:
        if product.category == "":
            print(product.variety)


# Sets all product 'photo' attributes to the correct file (webp or jpg)
# Depending on the actual file name stored in the product/photos (STATIC_ROOT)
def update_all_product_photos():

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
            product.photo = 'products/photos/default.jpg'

        product.save()


def product_has_image(image_path):
    # Use os.path.join to construct the absolute image path within STATIC_ROOT
    full_image_path = os.path.join(settings.STATIC_ROOT, image_path)
    return os.path.exists(full_image_path)


# # Function to change all backslashes to forward slashes in the photo attribute
def fix_slashes():
    products = Product.objects.all()
    for product in products:
        product.photo = product.photo.replace('\\', '/')
        product.save()

    print("slashes fixed")


def view_product_varieties():
    products = Product.objects.all()
    with open("ws_item_nums.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["item_number", "sku"])  # Write header row

        for product in products:
            cleaned_sku = product.sku.rstrip("w")  # Remove trailing 'w' if present
            writer.writerow([product.item_number, cleaned_sku])

    print("CSV file 'ws_item_nums.csv' created successfully.")
    return
    # Extract headers
    headers = ["Variety", "Category", "Super Type", "Veg Type", "Sub Type"]

    # Get all data and calculate the maximum width for each column
    data = [
        [product.variety, product.category, product.super_type, product.veg_type, product.sub_type]
        for product in products
    ]
    column_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]

    # Print the headers
    header_row = " | ".join(f"{headers[i]:<{column_widths[i]}}" for i in range(len(headers)))
    print(header_row)
    print("-" * len(header_row))  # Separator line

    # Print each product's details
    for row in data:
        print(" | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row))))

    # for product in products:

    #     print(product.variety, product.category, product.super_type, product.veg_type, product.sub_type)

def delete_duplicate_products():
    original_products = []
    products = Product.objects.all()
    for product in products:
        if product.item_number in original_products:
            print(product.variety, " deleted")
            product.delete()
        else:
            original_products.append(product.item_number)


def update_product_description(item_num, description):
   product = Product.objects.get(item_number=item_num)
   product.description = description
   product.save()
   print(f"The description for item number {product.item_number} has been updated to '{description}'")


def update_product_notes(item_num, notes):
   product = Product.objects.get(item_number=item_num)
   product.notes = notes
   product.save()
   print(f"The notes for item number {product.item_number} has been updated to '{notes}'")

def update_product_sub_type(item_num, sub_type):
   product = Product.objects.get(item_number=item_num)
   product.sub_type = sub_type
   product.save()
   print(f"The sub_type for item number {product.item_number} has been updated to '{product.sub_type}'")

def update_product_photo(item_num, photo):
    product = Product.objects.get(item_number=item_num)
    product.photo = photo
    product.save()
    print(f"The photo for item number {product.item_number} has been updated to '{product.photo}'")


def create_product_object(item_num,
                          sku,
                          notes,
                          category,
                          super_type,
                          veg_type,
                          sub_type,
                          variety,
                          description,
                          photo):

    product = Product.objects.create(
        item_number = item_num,
        sku = sku,
        notes = notes,
        active = '',
        category = category,
        super_type = super_type,
        veg_type = veg_type,
        sub_type = sub_type,
        variety = variety,
        description = description,
        quickbooks_code = '',
        photo = photo
    )

    product.save()
    print(f"{product.variety} added successfully")


# ####  MAIN PROGRAM BEGINS HERE  #### #

print_product_table()
# check_duplicate_item_numbers()

# update_notes_with_csv()
# check_categories()
# update_all_product_photos()
# fix_slashes()
# view_product_varieties()
# delete_duplicate_products()
# update_product_description(item_num, description)
# update_product_notes(item_num, notes)
# update_product_notes(383, '-')
# update_product_sub_type(341, 'PEONY')
# update_product_photo(item_num, photo)
# update_product_photo(203, "products/photos/203.jpg")

# create_product_object(440,
#                       "LET-SU-pktw",
#                       '-',
#                       'Vegetables',
#                       'LETTUCE',
#                       'LETTUCE',
#                       'CRISPHEAD',
#                       'Summertime',
#                       'Insanely crunchy iceberg variety that is the pinnacle of summer eating! Very slow to bolt.',
#                       'products/photos/443.jpg')



# EXAMPLE FOR CREATING PRODUCT OBJECT USING FUNCTION CALL ABOVE
# create_product_object(item_num,
                        # sku,
                        # notes,
                        # category,
                        # super_type,
                        # vegtype,
                        # sub_type,
                        # variety,
                        # description,
                        # photo)
# Examples:
    # category = 'VEGETABLES', 'FLOWERS', 'HERBS'
    # super_type = 'BEAN', 'BEET', 'BRASSICA', 'MISC', 'CARROT',
        # 'CORN & GRAIN', 'FLOWERS', 'TOMATO', 'PEPPER & EGGPLANT',
        # 'GREENS', 'SQUASH', 'CUKE & MELON', 'HERBS', 'PEA', 'ALLIUMS', 'LETTUCE'
    # veg_type = 'CABBAGE', 'SWEET PEA', 'FOUR O’CLOCK', 'TOMATO', 'LETTUCE', 'STRAWFLOWER', ETC
    # sub_type = 'DRY/BUSH', 'FAVA', 'NAPA', 'LOOSELEAF', ETC
