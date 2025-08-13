## Add a view function to input new products into the database from admin/add-products

from django.shortcuts import render
from stores.models import Store, StoreProduct
# from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.http import JsonResponse
import json
from orders.models import Order
from products.models import Product


def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# Handles requests from the admin user to edit the available products for a store
@login_required
@user_passes_test(is_admin)

def edit_products(request):
    if request.method == 'POST':
        # print("POST request received in edit_products view")
        # --- Selecting store - UPDATED ---
        if "store_id" in request.POST:
            store_id = request.POST.get('store_id')
            try:
                store = Store.objects.get(store_number=store_id)
                # Get all products that are available for this store from StoreProduct table
                available_item_numbers = list(
                    StoreProduct.objects.filter(
                        store=store, 
                        is_available=True
                    ).values_list('product__item_number', flat=True)
                )

                # print(f"Available item numbers for store {store_id}: {available_item_numbers}")
                available_item_numbers = [str(item) for item in available_item_numbers]
                return JsonResponse({'success': True, 'available_item_numbers': available_item_numbers})
            except Store.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Store not found'})
        
        # --- Save button clicked - UPDATED ---
        elif "store_handle" in request.POST:
            store_handle = request.POST.get('store_handle')
            store = Store.objects.get(store_number=store_handle)
            new_item_numbers = json.loads(request.POST.get('varieties'))  # list of item_numbers
            
            # Update StoreProduct table for this store
            # First, set all products for this store to not available
            StoreProduct.objects.filter(store=store).update(is_available=False)
            
            # Then set selected products to available
            for item_number in new_item_numbers:
                product = Product.objects.get(item_number=item_number)
                store_product, created = StoreProduct.objects.get_or_create(
                    store=store, 
                    product=product,
                    defaults={'is_available': True}
                )
                if not created:
                    store_product.is_available = True
                    store_product.save()
            
            return JsonResponse({'success': True})
        
        # --- Add items to all stores - UPDATED ---
        elif "varieties_to_add" in request.POST:
            varieties_to_add = json.loads(request.POST.get('varieties_to_add'))
            for store in Store.objects.all():
                for item_number in varieties_to_add:
                    product = Product.objects.get(item_number=item_number)
                    store_product, created = StoreProduct.objects.get_or_create(
                        store=store, 
                        product=product,
                        defaults={'is_available': True}
                    )
                    if not created:
                        store_product.is_available = True
                        store_product.save()
            return JsonResponse({'success': True})
        
        # --- Remove items from all stores - UPDATED ---
        elif "varieties_to_remove" in request.POST:
            varieties_to_remove = json.loads(request.POST.get('varieties_to_remove'))
            for store in Store.objects.all():
                for item_number in varieties_to_remove:
                    product = Product.objects.get(item_number=item_number)
                    StoreProduct.objects.filter(
                        store=store, 
                        product=product
                    ).update(is_available=False)
            return JsonResponse({'success': True})
        
        # --- Sync store from most recent order - UPDATED ---
        elif "store_to_sync" in request.POST:
            store_to_sync = json.loads(request.POST.get('store_to_sync'))
            store = Store.objects.get(store_number=store_to_sync)
            most_recent_order = Order.objects.filter(order_number__startswith=store_to_sync).order_by('-order_number').first()
            if most_recent_order:
                # First set all products for this store to not available
                StoreProduct.objects.filter(store=store).update(is_available=False)
                
                # Then set products from the order to available
                products_in_order = most_recent_order.products.all()
                for product in products_in_order:
                    store_product, created = StoreProduct.objects.get_or_create(
                        store=store, 
                        product=product,
                        defaults={'is_available': True}
                    )
                    if not created:
                        store_product.is_available = True
                        store_product.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        # GET request → render form with seed availabilities for first store (optional)
        products = Product.objects.all().order_by('category', 'veg_type', 'variety')
        # exclude stores whose name starts with "PCC"
        stores = Store.objects.exclude(name__startswith="PCC").all()
        veg_types = products.order_by('veg_type').values_list('veg_type', flat=True).distinct()
        veg_types = list(veg_types)
        context = {
            'products': products,
            'stores': stores,
            'veg_types': veg_types,
        }
        return render(request, 'products/edit_products.html', context)









# def edit_products(request):
#     # print("inside edit_product_availailities view function")
#     if request.method == 'POST':

#         # Selecting store from dropdown
#         if "store_id" in request.POST:
#             try:
#                 store_id= request.POST.get('store_id')
#                 store = Store.objects.get(store_number=store_id)
#                 # print("first IF")#, store.available_products)
#                 available_varieties = [variety for variety, is_available in store.available_products.items() if is_available]
#                 # print ("available_varieties: ", available_varieties)
#                 response_data = {
#                     'success': True,
#                     'available_varieties': available_varieties
#                 }
#             except Store.DoesNotExist:
#                 form = ProductForm()
#                 # print("store does not exist")
#                 # response_data = {'success': False, 'error': 'Store not found'}

#             return JsonResponse(response_data)

#         # Save button is clicked
#         elif "store_handle" in request.POST:
#             # look up store by store_handle
#             store_handle = request.POST.get('store_handle')
#             # print("store_handle: ", store_handle)
#             store = Store.objects.get(store_number=store_handle)
#             # print("store: ", store.name)
#             new_product_availabilities = request.POST.get('varieties')
#             # process the 'varieties' stringified dict and update the store's available products
#             new_product_availabilities_dict = json.loads(new_product_availabilities)
#             # Updating the store's available products
#             for variety, is_available in new_product_availabilities_dict.items():
#                 if variety in store.available_products:
#                     store.available_products[variety] = is_available
#                     # print("variety: ", variety)
#                 # else:
#                     # print("variety not found")
#             store.save()

#             return JsonResponse({'success': True})
#         #add button is clicked to add items to all stores' available products dicts
#         elif "varieties_to_add" in request.POST:
#             #get the list of items to add
#             varieties_to_add = json.loads(request.POST.get('varieties_to_add'))
#             # print("varieties_to_add: ", varieties_to_add)
#             #loop through the stores and add the items to each store's available products dict

#             # Iterate through all store objects
#             for store in Store.objects.all():
#             # Update the available_products dictionary for each store
#                 for variety in varieties_to_add:
#                     store.available_products[variety] = True

#                 # Save the updated store object
#                 store.save()

#             return JsonResponse({'success': True})

#         elif "varieties_to_remove" in request.POST:
#             # print("removing items from all stores")
#             #get the list of items to remove
#             varieties_to_remove = json.loads(request.POST.get('varieties_to_remove'))
#             #loop through the stores and remove the items from each store's available products dict
#             # print("varieties_to_remove: ", varieties_to_remove)
#             # Iterate through all store objects
#             for store in Store.objects.all():
#             # Update the available_products dictionary for each store
#                 for variety in varieties_to_remove:
#                     # print("variety: ", variety)
#                     store.available_products[variety] = False

#                     # Save the updated store object
#                 store.save()

#             return JsonResponse({'success': True})

#         elif "store_to_sync" in request.POST:

#             # get the store to sync based on the store number
#             store_to_sync = json.loads(request.POST.get('store_to_sync'))

#             # get the store object
#             store = Store.objects.get(store_number=store_to_sync)

#             # get the store's previous order
#             most_recent_order = Order.objects.filter(order_number__startswith=store_to_sync).order_by('-order_number').first()
#             # print(most_recent_order.order_number)

#             if most_recent_order:
#                 products_in_order = most_recent_order.products  # Get the products from the most recent order
#                 product_availabilities = store.available_products

#                 # Iterate through the product_availabilities dictionary
#                 for product_number in product_availabilities.keys():
#                     # Check if the product is in the most recent order's products
#                     if product_number in products_in_order:
#                         product_availabilities[product_number] = True
#                     else:
#                         product_availabilities[product_number] = False

#                 # Update the store's product_availabilities
#                 store.available_products = product_availabilities
#                 store.save()

#             return JsonResponse({'success': True})

#         else:
#             print("NON-Sense")
#             return JsonResponse({'success': False})


#     else:
#         form = ProductForm()

#     # Render the form with the current available varieties
#     context = {
#         'form': form,
#         #'available_varieties': available_varieties
#     }


#     return render(request, 'products/edit_products.html', context)

