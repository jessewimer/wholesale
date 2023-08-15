from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    #path('login/', views.store_login, name='login'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    #path('stores/dashboard/', views.dashboard, name='dashboard'),
]
#path('profile/', views.profile_view, name='profile'),