#import pandas as pd
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

from django.contrib.auth.models import User
from stores.models import Store


def set_store_usernames():
    username_dict={
        10: 'alberta',
        11: 'blossom',
        12: 'central',
        13: 'christiansons',
        14: 'cloudmountain',
        15: 'cordata',
        16: 'downtown',
        17: 'concentrates',
        18: 'crossroads',
        19: 'foodfront',
        20: 'mainmarket',
        21: 'mountaincommunity',
        22: 'mygarden',
        23: 'olympiaeast',
        24: 'olympiawest',
        25: 'orcascoop',
        26: 'pcccentral',
        27: 'pccballard',
        28: 'pccbothell',
        29: 'pccburien',
        30: 'pcccolumbiacity',
        31: 'pccedmonds',
        32: 'pccfremont',
        33: 'pccaurora',
        34: 'pccgreenlake',
        35: 'pccissaquah',
        36: 'pcckirkland',
        37: 'pccredmond',
        38: 'pccviewridge',
        39: 'pccwestseattle',
        40: 'peoplescoop',
        41: 'porttownsendcoop',
        42: 'sanjuancoop',
        43: 'skagitcoop',
        44: 'snoislecoop',
        45: 'sundance',
        46: 'walts',
    }
    for store in Store.objects.all():
        store.username = username_dict[store.store_number]
        store.save()

def delete_user_object():
    
    for user in User.objects.all():
        if user.username == 'username':
            user.delete()

def clear_stores_total_orders():
    for store in Store.objects.all():
        store.total_orders = 0
        store.total_num_packets = 0
        store.save()



def create_users_for_stores():

    # Retrieve store #10
    store = Store.objects.get(store_number=10)
   # user = User.objects.create_user(username=store.username, password=store.password)
   # store.store_user = user
    store.total_orders = 0
    store.save()
    # Retrieve all instances of the Store model
    # stores = Store.objects.all()

    # for store in stores:
    #     if store.store_number == 10:
    #         store.username = 'alberta'
    #         store.password = 'Uprising@10!'
    #         store.save()
        
    #     user = User.objects.create_user(username=store.username, password=store.password)
    #     store.store_user = user
    #     store.save()
    #     print(store.name, "has been updated with a user object.")



        # # Check if the store has a username and password
        # if store.username and store.password:
        #     # Check if the store already has an associated User object
        #     if not store.store_user:
        #         # Create a new User object using the store's username and password
        #         user = User.objects.create_user(username=store.username, password=store.password)
                
        #         # Associate the user with the store
        #         store.store_user = user
        #         store.save()
        #         print(store.name, "has been updated with a user object.")



# Function to set all stores' passwords to f("Uprising@{store_number}!")
def set_store_passwords():
    # Retrieve all instances of the Store model
    stores = Store.objects.all()

    for store in stores:
        store.password = ""
        
        store.save()


# Function to set all stores' available_products to a dictionary with item numbers as keys and True as values
def set_store_products():
    # Retrieve all store objects
    stores = Store.objects.all()

    # Create a dictionary with item numbers as keys and True as values
    item_numbers = {num: True for num in range(101, 392)}

    for store in stores:
        store.available_products = item_numbers
        store.save()

    print("All stores have been updated with the full list of products.")


# Function to modifiy a store's avaialble_products dictionary for testing purposes
def modify_store_products(store_number):
    # Retrieve the store object
    store = Store.objects.get(store_number=store_number)
    i = 0
    # For loop to set all items to true that have keys less that 125
    for item in store.available_products:
        # if i is even, set the item to false
        if i % 2 == 0:
            store.available_products[item] = True
            store.save()
        i += 1
        # if int(item) < 125:
            # store.available_products[item] = False
            # store.save()
    print("Store number", store_number, "has been updated with all true values.")

#modify_store_products(11)

# if __name__ == '__main__':
#     create_users_for_stores()
#     print("Users created successfully.")

# set_store_passwords()

#set_store_usernames()

#delete_user_object()

#clear_stores_total_orders()

# set_store_products()