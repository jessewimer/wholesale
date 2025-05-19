from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm
from .models import Store
from products.models import Product
import json
from orders.models import Order
from orders.auto_email import send_email
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string


class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomLoginView(LoginView):
    def get_success_url(self):
        store_name = self.request.user.store.username
        return reverse('dashboard', kwargs={'store_name': store_name})


@login_required
def dashboard(request, store_name):
    user = request.user
    store = Store.objects.get(store_user=user)

    # Get all products in the database (not just the ones associated with the store)
    # all_products = Product.objects.all()

    # Create a dictionary of product item numbers as keys and their corresponding variety names as values
    # product_dict = {
    #     product.item_number: [product.variety, product.veg_type]
    #     for product in all_products
    # }

    # for item_number, details in product_dict.items():
    #     variety = details[0]
    #     veg_type = details[1]
    #     print(f"Item Number: {item_number}, Variety: {variety}, Veg Type: {veg_type}")


    if request.method == 'POST':
        # Process the form submission
        order_data = json.loads(request.body)
        invalid_products = []
        print("ORDER DATA: ", order_data)
        for product_number in order_data.keys():
            if not store.available_products.get(product_number, False):
                invalid_products.append(product_number)
        print("NEW invalid products :", invalid_products)
        if invalid_products:
            print("NEW inside invalid_products")

            return JsonResponse({'invalid_products': invalid_products}, status=400)

        # Create a new order
        print("Store: ", store)
        order = Order.build_order(order_data, store)

        # send_email(order)

        # Redirect back to the dashboard page
        return redirect('dashboard', store_name=store_name)

    # Getting the previously ordered items associated with the store
    previous_orders = Order.objects.filter(order_number__startswith=store.store_number)
    previous_items = []
    for order in previous_orders:
        for item_number in order.products.keys():
            if item_number not in previous_items:
                previous_items.append(item_number)


    product_numbers = [product_number for product_number, is_available in store.available_products.items() if is_available]
    products = Product.objects.filter(item_number__in=product_numbers)

    context = {

        'store': store,
        'products': products,
        'slots': store.slots,
        'previous_items': previous_items,
    }

    return render(request, 'stores/dashboard.html', context)
