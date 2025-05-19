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

from orders.models import Order
# from products.models import Product

# Deletes all order from the database
def delete_orders():
    orders = Order.objects.all()
    for order in orders:
        order.delete()
    print('orders deleted')

    # print("total costs")
    # for order in orders:
    #     print(order.total_cost)


def view_orders():
    orders = Order.objects.all()
    for order in orders:
        print("current order: ", order.order_number, " - ", order.order_date)

    print("End of list")

def view_single_store_orders(store_num):
    orders = Order.objects.all()
    # for order in orders:
    #     if order.order_number.startswith(store_num):
    #         print(order.order_number)
    for order in orders:
        order_number_str = str(order.order_number)
        store_num_str = str(store_num)
        if order_number_str.startswith(store_num_str):
            print(order.order_date, order_number_str)
            print("products:")
            print(order.products)

# delete_orders()

# view_orders()
view_single_store_orders(49)






