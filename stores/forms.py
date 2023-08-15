from django import forms
from .models import Store

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

# class StoreForm(forms.ModelForm):
#     class Meta:
#         model = Store
#         fields = ['name', 'available_products']

#     # Add a widget to make the available_products field appear as checkboxes
#     available_products = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
