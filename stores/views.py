from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .models import Store
from products.models import Product
import json
from orders.models import Order, OrderIncludes
# from orders.auto_email import send_email
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
import pytz
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

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
    current_year = settings.CURRENT_ORDER_YEAR
    year_suffix = f"{current_year % 100:02d}"
    pkt_price = settings.PACKET_PRICE

    if request.method == 'POST':
        # Process the form submission
        order_data = json.loads(request.body)
        invalid_products = []
        # print("ORDER DATA: ", order_data)

        # Check for invalid products
        for product_number in order_data.keys():
            try:
                # Convert product_number to integer since it comes as string from JSON
                product_number_int = int(product_number)
                # Check if the product exists in the store's available products
                if not store.available_products.filter(item_number=product_number_int).exists():
                    invalid_products.append(product_number)
            except (ValueError, TypeError):
                # Handle cases where product_number can't be converted to int
                invalid_products.append(product_number)

        if invalid_products:
            # print("NEW inside invalid_products")
            return JsonResponse({'invalid_products': invalid_products}, status=400)

        existing_orders = Order.objects.filter(store=store, order_number__endswith=f"-{year_suffix}")
        this_year_order_count = existing_orders.count() + 1

        pacific_tz = pytz.timezone('US/Pacific')
        pacific_now = timezone.now().astimezone(pacific_tz).date()

        order = Order.objects.create(
            store=store,
            order_number = f"W{store.store_number:02d}{this_year_order_count:02d}-{year_suffix}",
            order_date=pacific_now,
        )

        # Create OrderIncludes entries for each product in the order
        for item_number, quantity in order_data.items():
            try:
                product = Product.objects.get(item_number=item_number)
                OrderIncludes.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=pkt_price,
                )
            except Product.DoesNotExist:
                print(f"Product with item_number {item_number} does not exist")
                continue
        # send_email(order)
        # Return success response for AJAX
        return JsonResponse({'status': 'success'}, status=200)

    # Get all orders for the current year for this store
    current_year_orders = Order.objects.filter(
        store=store,
        order_number__endswith=f"-{year_suffix}"
    ).select_related('store').prefetch_related('orderincludes_set__product').order_by('-order_date')

    # Get previous items with total quantity per product
    previous_orders = (
        OrderIncludes.objects
        .filter(order__store=store)
        .values('product__item_number')
        .annotate(total_qty=Sum('quantity'))
    )
    # Convert to dictionary: { 'item_number': quantity }
    previous_items_dict = {
        entry['product__item_number']: entry['total_qty']
        for entry in previous_orders
    }

    # Get all available products for the store
    products = Product.objects.filter(
        available_in_stores=store,
        storeproduct__is_available=True
    )
    # Attach `.previously_ordered_count` to each product
    for product in products:
        product.previously_ordered_count = previous_items_dict.get(product.item_number, 0)

    # Prepare orders data for JavaScript (if needed)
    orders_data = []
    for order in current_year_orders:
        order_items = []
        for order_include in order.orderincludes_set.all():
            order_items.append({
                'item_number': order_include.product.item_number,
                'variety': order_include.product.variety,
                'quantity': order_include.quantity,
                'price': float(pkt_price)
            })

        orders_data.append({
            'id': order.id,
            'order_number': order.order_number,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'items': order_items,
            'total_items': sum(item['quantity'] for item in order_items),
            'total_cost': sum(item['quantity'] for item in order_items) * pkt_price
        })

    # for order in orders_data:
    #     print(f"Order ID: {order['id']}, Order Num: {order['order_number']}, Total Cost: {order['total_cost']}")

    product_qs = Product.objects.all().values('item_number', 'variety', 'veg_type')
    product_dict = {}

    for p in product_qs:
        item_num = p['item_number']
        # Skip if item_number is None or missing variety/veg_type to avoid bad entries
        if item_num is not None and p['variety'] and p['veg_type']:
            product_dict[item_num] = [p['variety'], p['veg_type']]


    product_dict_json = json.dumps(product_dict)

    context = {
        'store': store,
        'products': products,
        'slots': store.slots,
        'previous_items': json.dumps(previous_items_dict),  # still useful for JS
        'current_year_orders': orders_data,
        'orders_data': json.dumps(orders_data),  # JSON data for JavaScript
        'current_year': current_year,
        'year_suffix': year_suffix,
        'pkt_price': pkt_price,
        'product_dict_json': product_dict_json,
    }
    return render(request, 'stores/dashboard.html', context)


@login_required
def process_store_orders(request):
    """
    View for processing wholesale orders
    """
    context = {
        'page_title': 'Process Orders',
        # Add placeholder data - replace with real data later
        'pending_orders': [
            {
                'order_id': 'WO-2024-001',
                'store_name': 'Green Thumb Garden Center',
                'date': '2024-08-10',
                'total_packets': 150,
                'status': 'pending'
            },
            {
                'order_id': 'WO-2024-002', 
                'store_name': 'Urban Seeds Co.',
                'date': '2024-08-12',
                'total_packets': 75,
                'status': 'processing'
            },
        ],
        'total_pending': 2,
        'total_packets': 225,
    }
    
    return render(request, 'stores/store_orders.html', context)

@login_required
def view_stores(request):
    """
    View for displaying all store locations and their details
    """
    # fetch all store objects from the database, excluding ones whose name attribute start with "PCC"
    stores = Store.objects.exclude(name__startswith="PCC")
    context = {'stores': stores}
    
    return render(request, 'stores/view_stores.html', context)


@require_http_methods(["POST"])
def update_store(request, store_num):
    print(f"Updating store with number: {store_num}")
    try:
        # Get the store object
        store = get_object_or_404(Store, store_number=store_num)
        
        # Parse the JSON data from the request
        data = json.loads(request.body)
        
        # Update the store fields
        if 'name' in data:
            store.name = data['name']
        if 'email' in data:
            store.email = data['email']
        if 'slots' in data:
            store.slots = int(data['slots']) if data['slots'] else None
        if 'contact_name' in data:
            store.contact_name = data['contact_name']
        
        # Save the changes to the database
        store.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Store updated successfully'
        })
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in update_store: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)