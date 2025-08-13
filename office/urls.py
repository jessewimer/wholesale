from django.urls import path
from .views import OfficeLoginView, OfficeLogoutView, office_dashboard
# from django.contrib.auth.views import LogoutView
from .views import varieties_json, inventory_germination, crops_json, products_by_crop_json
# import office.views as office_views
import products.views as product_views

urlpatterns = [
    path('login/', OfficeLoginView.as_view(), name='office_login'),
    path('dashboard/', office_dashboard, name='office_dashboard'),
    path('logout/', OfficeLogoutView.as_view(), name='office_logout'),
    path('inventory-germination/', inventory_germination, name='inventory_germination'),
    path('edit-products/', product_views.edit_products, name='edit_products'),
    path('varieties-json/', varieties_json, name='varieties_json'),
    path("crops-json/", crops_json, name="crops_json"),
    path('inventory-germination/<str:crop>/', products_by_crop_json, name='products_by_crop_json'),
]
