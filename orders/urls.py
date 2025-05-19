from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet



router = routers.DefaultRouter()
router.register(r'order-data', OrderViewSet)

urlpatterns = [
    # Other URL patterns
    path('api/', include(router.urls)),
]
