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

class CustomLoginView(LoginView):
    def get_success_url(self):
        store_name = self.request.user.store.username
        return reverse('dashboard', kwargs={'store_name': store_name})


class CustomLogoutView(LogoutView):
    next_page = 'login' 

@login_required
def dashboard(request, store_name):
    user = request.user
    store = Store.objects.get(store_user=user)

    if request.method == 'POST':
        # Process the form submission
        order_data = json.loads(request.body)
        # Create a new order
        order = Order.build_order(order_data, store)
        #print('before send email')
        send_email(order)
        #print('after send email')   


        # Redirect back to the dashboard page
        return redirect('dashboard', store_name=store_name) 
    
    product_numbers = [product_number for product_number, is_available in store.available_products.items() if is_available]
    products = Product.objects.filter(item_number__in=product_numbers)

    # Retrieve additional customer-related information from the user or associated models
    
    context = {
        'store': store,
        'products': products,
    }
    
    return render(request, 'stores/dashboard.html', context)
