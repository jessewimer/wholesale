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

@login_required
def dashboard(request):

    user = request.user
    store = Store.objects.get(store_user=user)

    if request.method == 'POST':
        # Process the form submission
        order_data = json.loads(request.body)
        # Create a new order
        order = Order.build_order(order_data, store)
    
        send_email(order)

        # Display a success message
        messages.success(request, 'Order submitted successfully.')

        # Redirect back to the dashboard page
        return redirect('dashboard') 
    
    product_numbers = [product_number for product_number, is_available in store.available_products.items() if is_available]
    products = Product.objects.filter(item_number__in=product_numbers)

    # Retrieve additional customer-related information from the user or associated models
    
    context = {
        'store': store,
        'products': products,
    }
    
    return render(request, 'stores/dashboard.html', context)
