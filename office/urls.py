# from django.urls import path
# from .views import OfficeLoginView, OfficeLogoutView, office_dashboard
# # from django.contrib.auth.views import LogoutView
# from .views import varieties_json, inventory_germination, crops_json, products_by_crop_json
# # import office.views as office_views
# import products.views as product_views

# urlpatterns = [
#     path('login/', OfficeLoginView.as_view(), name='office_login'),
#     path('dashboard/', office_dashboard, name='office_dashboard'),
#     path('logout/', OfficeLogoutView.as_view(), name='office_logout'),
#     path('inventory-germination/', inventory_germination, name='inventory_germination'),
#     path('edit-products/', product_views.edit_products, name='edit_products'),
#     path('varieties-json/', varieties_json, name='varieties_json'),
#     path("crops-json/", crops_json, name="crops_json"),
#     path('inventory-germination/<str:crop>/', products_by_crop_json, name='products_by_crop_json'),
# ]
from django.urls import path
from .views import OfficeLoginView, OfficeLogoutView, office_dashboard, office_landing, view_variety
from .views import varieties_json, inventory_germination, crops_json, products_by_crop_json
import products.views as product_views

urlpatterns = [
    # Authentication
    path('login/', OfficeLoginView.as_view(), name='office_login'),
    path('logout/', OfficeLogoutView.as_view(), name='office_logout'),
    
    # Main office pages
    # path('', office_landing, name='office_landing'),  # This was missing!
    path('dashboard/', office_landing, name='office_landing'),
    
    # Action card destinations (matching the landing page links)
    path('edit-products/', product_views.edit_products, name='edit_products'),
    path('view-variety/', view_variety, name='view_variety'),  # New view
    path('inventory/', inventory_germination, name='inventory'),  # Updated name to match landing page
    
    # Keep your existing inventory page with original name for backward compatibility
    path('inventory-germination/', inventory_germination, name='inventory_germination'),
    
    # JSON API endpoints
    path('varieties-json/', varieties_json, name='varieties_json'),
    path("crops-json/", crops_json, name="crops_json"),
    path('inventory-germination/<str:crop>/', products_by_crop_json, name='products_by_crop_json'),
]