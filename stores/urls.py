from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [  
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('<str:store_name>/', views.dashboard, name='dashboard'),
]
