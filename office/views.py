from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render
from .decorators import brian_login_required, login_required
from django.http import JsonResponse
# change to Variety in production
from products.models import Product


class OfficeLoginView(LoginView):
    template_name = 'office/login.html'           # Custom template
    redirect_authenticated_user = True             # Redirect if already logged in
    
    def get_success_url(self):
        # Redirect to office landing page after login
        return reverse_lazy('office_landing')


class OfficeLogoutView(LogoutView):
    next_page = 'office_login'


# @brian_login_required
def office_landing(request):
    """
    Office landing page view - displays the main office portal with action cards
    """
    context = {
        'user': request.user,
        'user_name': request.user.get_full_name() or request.user.username,
    }
    
    return render(request, 'office/office_landing.html', context)


@brian_login_required
def office_dashboard(request):
    """
    Main office dashboard - your existing edit products functionality
    """
    return render(request, 'office/office_dashboard.html')


@brian_login_required
def inventory_germination(request):
    """
    Inventory and germination tracking view
    """
    return render(request, 'office/inventory_germination.html')


@brian_login_required
def view_variety(request):
    """
    View all varieties - new view for the landing page action card
    """
    # Get all products with their varieties
    products = Product.objects.exclude(variety__isnull=True).exclude(variety='').order_by('veg_type', 'variety')
    
    context = {
        'products': products,
    }
    
    return render(request, 'office/view_variety.html', context)



@login_required
def analytics(request):
    """
    View for displaying analytics and business performance metrics
    """
    context = {
        'page_title': 'Analytics Dashboard',
        # Add any data you want to pass to the template
        # For example:
        # 'sales_data': get_sales_data(),
        # 'inventory_metrics': get_inventory_metrics(),
        # 'popular_products': get_popular_products(),
    }
    
    # Render the template from the products app
    return render(request, 'products/analytics.html', context)

# JSON API endpoints
@brian_login_required
def varieties_json(request):
    """
    Get distinct non-null, non-empty varieties as JSON
    """
    varieties = Product.objects.exclude(variety__isnull=True).exclude(variety='').values_list('variety', flat=True).distinct()
    data = [{"name": v} for v in varieties]
    return JsonResponse(data, safe=False)


@brian_login_required
def crops_json(request):
    """
    Get crops/veg_types as JSON with optional search
    """
    q = request.GET.get('q', '')
    crops = Product.objects.exclude(veg_type__isnull=True).exclude(veg_type='')
    
    if q:
        crops = crops.filter(veg_type__icontains=q)
    
    crop_names = crops.values_list('veg_type', flat=True).distinct()
    data = [{"name": name} for name in crop_names]
    return JsonResponse(data, safe=False)


@brian_login_required
def products_by_crop_json(request, crop):
    """
    Get products by specific crop/veg_type as JSON
    """
    products = Product.objects.filter(veg_type=crop)
    data = []
    
    for p in products:
        data.append({
            "veg_type": p.veg_type,
            "variety": p.variety,
            "current_inventory": "-",
            "previous_inventory": "-",
            "difference": "-",
            "germ_23": "-",
            "germ_24": "-",
            "germ_25": "-"
        })
    
    return JsonResponse(data, safe=False)