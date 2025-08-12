from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render
from .decorators import brian_login_required
from django.http import JsonResponse

# change to Variety in production
from products.models import Product

class OfficeLoginView(LoginView):
    template_name = 'office/login.html'           # Custom template
    redirect_authenticated_user = True             # Redirect if already logged in

    def get_success_url(self):
        # Redirect to office dashboard after login
        return reverse_lazy('office_dashboard')

@brian_login_required
def office_dashboard(request):
    return render(request, 'office/office_dashboard.html')

@brian_login_required
def inventory_germination(request):
    return render(request, 'office/inventory_germination.html')

@brian_login_required
def varieties_json(request):
    # Get distinct non-null, non-empty varieties
    varieties = Product.objects.exclude(variety__isnull=True).exclude(variety='').values_list('variety', flat=True).distinct()

    data = [{"name": v} for v in varieties]

    return JsonResponse(data, safe=False)

@brian_login_required
def crops_json(request):
    q = request.GET.get('q', '')
    crops = Product.objects.exclude(veg_type__isnull=True).exclude(veg_type='')

    if q:
        crops = crops.filter(veg_type__icontains=q)

    crop_names = crops.values_list('veg_type', flat=True).distinct()
    data = [{"name": name} for name in crop_names]

    return JsonResponse(data, safe=False)

@brian_login_required
def products_by_crop_json(request, crop):
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

