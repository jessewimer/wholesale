from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

def get_store_by_number(store_number):
    # Retrieve the store object or raise a 404 error if it doesn't exist
    store = get_object_or_404(Store, store_number=store_number)
    return store

@login_required
def order_submission(request):
    from .auto_email import send_email
    if request.method == 'POST':
        # Retrieve the data from the submitted form
        seed_varieties = request.POST.getlist('products')
        quantities = request.POST.getlist('quantities')
        store_number = request.user.customer.customer_number
        store = get_store_by_number(store_number)
        
        # Convert the data into a dictionary
        seed_dict = dict(zip(seed_varieties, quantities))
         
        # Call the function to build the order, passing the seed dictionary/customer id
        order = Order.build_order(seed_dict, store)

        # email to store owner
        send_email(order)
    return render(request, 'order_confirmation.html', context)

def create_order(request):
    # Retrieve order information from the form 
    # Retrieve customer information from the form or API request
    customer_id = request.POST.get('customer_id')
    
    

    # Get the order total from the 

    # Retrieve the customer object based on the customer_id
    customer = get_object_or_404(Customer, pk=customer_id)
    
    customer.add_order(100)
   
    
    
    
    
    return HttpResponse('Order created successfully')

