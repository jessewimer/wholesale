## Add a view function to input new products into the database from admin/add-products

from django.shortcuts import render
from stores.models import Store
from .forms import ProductForm 
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.http import JsonResponse
import json

def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# Handles requests from the admin user to edit the available products for a store
@login_required
@user_passes_test(is_admin)
def edit_product_availabilities(request):

    if request.method == 'POST':
        
        # Selecting store from dropdown
        if "store_id" in request.POST:
            try:
                store_id= request.POST.get('store_id')
                store = Store.objects.get(store_number=store_id)
                # print("first IF")#, store.available_products)
                available_varieties = [variety for variety, is_available in store.available_products.items() if is_available]
                #print ("available_varieties: ", available_varieties)
                response_data = {
                    'success': True,
                    'available_varieties': available_varieties
                }
            except Store.DoesNotExist:
                form = ProductForm()
                # print("store does not exist")
                # response_data = {'success': False, 'error': 'Store not found'}
            
            return JsonResponse(response_data)
          
        # Save button is clicked 
        elif "store_handle" in request.POST:
            # look up store by store_handle
            store_handle = request.POST.get('store_handle')
            # print("store_handle: ", store_handle)
            store = Store.objects.get(store_number=store_handle)
            # print("store: ", store.name)
            new_product_availabilities = request.POST.get('varieties')
            # process the 'varieties' stringified dict and update the store's available products
            new_product_availabilities_dict = json.loads(new_product_availabilities)
            # Updating the store's available products
            for variety, is_available in new_product_availabilities_dict.items():
                if variety in store.available_products:
                    store.available_products[variety] = is_available
                    # print("variety: ", variety)
                # else:
                    # print("variety not found")       
            store.save()


            #form = ProductForm(request.POST, available_varieties=)

            # if form.is_valid():
            #     # Process the form data and update the store's available products
            #     selected_varieties = form.cleaned_data['selected_varieties']
            #     for variety in available_varieties:
            #         if variety in selected_varieties:
            #             store.available_products[variety] = True
            #         else:
            #             store.available_products[variety] = False

            #     # Save the updated store
            #     store.save()
            #     print("processing form data")
            #     # Redirect edit_store_availabilities
            #     return redirect('edit_product_availabilities')
            
            
            return JsonResponse({'success': True})
        #add button is clicked to add items to all stores' available products dicts
        elif "varieties_to_add" in request.POST:
            #get the list of items to add
            varieties_to_add = json.loads(request.POST.get('varieties_to_add'))
            # print("varieties_to_add: ", varieties_to_add)
            #loop through the stores and add the items to each store's available products dict
            
            # Iterate through all store objects
            for store in Store.objects.all():
            # Update the available_products dictionary for each store
                for variety in varieties_to_add:
                    store.available_products[variety] = True
                
                # Save the updated store object
                store.save()
      
            return JsonResponse({'success': True})
        
        elif "varieties_to_remove" in request.POST:
            # print("removing items from all stores")
            #get the list of items to remove
            varieties_to_remove = json.loads(request.POST.get('varieties_to_remove'))
            #loop through the stores and remove the items from each store's available products dict
            # print("varieties_to_remove: ", varieties_to_remove)
            # Iterate through all store objects
            for store in Store.objects.all():
            # Update the available_products dictionary for each store
                for variety in varieties_to_remove:
                    # print("variety: ", variety)
                    store.available_products[variety] = False
                
                    # Save the updated store object
                store.save()
    
            return JsonResponse({'success': True})
        
        else: 
            print("NON-Sense")
            return JsonResponse({'success': False})
    else:
        form = ProductForm()
    # Render the form with the current available varieties
    context = {
        'form': form,
        #'available_varieties': available_varieties
    }
    #print("rendering HTML")
    return render(request, 'products/products_list.html', context)

