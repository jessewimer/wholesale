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

from orders.models import Order, OrderIncludes

def view_order_includes(store_num):

    pass

# Deletes all order from the database
def delete_orders():
    orders = Order.objects.all()
    for order in orders:
        order.delete()
    print('orders deleted')



def view_orders():
    orders = Order.objects.all()
    for order in orders:
        print("current order: ", order.order_number, " - ", order.order_date)

    print("End of list")

def view_single_store_orders(store_num):
    orders = Order.objects.all()
    for order in orders:
        order_number_str = str(order.order_number)
        store_num_str = str(store_num)
        if order_number_str.startswith(store_num_str):
            print(order.order_date, order_number_str)
            print("products:")
            for include in order.orderincludes_set.all():
                print(f"- {include.product.variety} ({include.product.veg_type}) x {include.quantity}")


# from orders.models import OrderIncludes
# from stores.models import Store

# store = Store.objects.get(store_user__username="pccballard")  # adjust as needed
# includes = OrderIncludes.objects.filter(order__store=store)
# for i in includes:
#     print(i.product.item_number, i.order.order_number)




delete_orders()

# view_orders()
# view_single_store_orders(27)






