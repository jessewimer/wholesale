from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm

def login(request):
    #check to see if the store has submitted login credentials
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Custom authentication logic (example)
            if username == 'admin' and password == 'password':
                # If authentication is successful, redirect to the dashboard
                return redirect('dashboard')
            else:
                # If authentication fails, display an error message
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'stores/login.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    # Retrieve additional customer-related information from the user or associated models
    # Perform any other necessary operations
    
    context = {
        'store_name': store_name,
        # Add any other context variables required for rendering the template
    }
    
    return render(request, 'stores/dashboard.html', context)

@login_required
def place_order(request):
    # Handle the order placement form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Process the order and save it to the database
            return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'stores/place_order.html', {'form': form})
