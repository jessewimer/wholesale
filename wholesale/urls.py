"""wholesale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from stores.views import login, dashboard
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stores.urls')),
    
    path('', lambda request: redirect('login/', permanent=False)),
    
    
    
    #path('dashboard/', dashboard, name='dashboard'),
    # path('', login, name='login')
    # path('dashboard/', dashboard, name='login')

    #path("stores/", include('stores.urls')),
    #path("login/", include('django.contrib.auth.urls')), 
    #path("dashboard/", store_views.dashboard, name="dashboard"),
]