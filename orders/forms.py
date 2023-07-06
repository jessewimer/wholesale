from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_packets', 'total_cost', 'order_number', 'store']

    # Add any additional form validation or customizations if necessary