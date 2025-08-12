# from django.conf import settings
# from django.shortcuts import render
# from django.urls import resolve

# class MaintenanceModeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if getattr(settings, 'SITE_MAINTENANCE_MODE', False):
#             # Allow access to staff/admins
#             if request.user.is_authenticated and request.user.is_staff:
#                 return self.get_response(request)

#             # Allow access to specific username "billiard"
#             if request.user.is_authenticated and request.user.username == 'pccballard':
#                 return self.get_response(request)

#             # Allow access to login or admin login pages
#             try:
#                 if resolve(request.path_info).url_name in ['login', 'admin:login']:
#                     return self.get_response(request)
#             except:
#                 pass  # fallback in case path doesn't resolve

#             # Show maintenance message to everyone else
#             return render(request, 'stores/maintenance.html', status=503)

#         return self.get_response(request)


# from django.conf import settings
# from django.shortcuts import render
# from django.urls import resolve

# class MaintenanceModeMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if getattr(settings, 'SITE_MAINTENANCE_MODE', False):
#             # ✅ Allow access to API endpoints (starts with /orders/api/)
#             if request.path.startswith('/orders/api/'):
#                 return self.get_response(request)

#             # ✅ Allow access to staff/admins
#             if request.user.is_authenticated and request.user.is_staff:
#                 return self.get_response(request)

#             # ✅ Allow access to specific username
#             if request.user.is_authenticated and request.user.username == 'pccballard':
#                 return self.get_response(request)

#             # ✅ Allow access to login or admin login pages
#             try:
#                 if resolve(request.path_info).url_name in ['login', 'admin:login']:
#                     return self.get_response(request)
#             except:
#                 pass  # fallback in case path doesn't resolve

#             # ❌ Show maintenance message to everyone else
#             return render(request, 'stores/maintenance.html', status=503)

#         return self.get_response(request)

from django.conf import settings
from django.shortcuts import render
from django.urls import resolve, Resolver404

class MaintenanceModeMiddleware:
    ALLOWED_USERS = {'pccballard'}  # Add more usernames if needed

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'SITE_MAINTENANCE_MODE', False):
            # Allow API requests
            if request.path.startswith('/orders/api/'):
                return self.get_response(request)

            # Allow static and media files (optional, adjust paths as needed)
            if request.path.startswith(settings.STATIC_URL) or request.path.startswith('/media/'):
                return self.get_response(request)

            # Allow staff/admin users
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)

            # Allow specific allowed usernames
            if request.user.is_authenticated and request.user.username in self.ALLOWED_USERS:
                return self.get_response(request)

            # Allow login and admin login pages
            try:
                url_name = resolve(request.path_info).url_name
            except Resolver404:
                url_name = None

            if url_name in ['login', 'admin:login']:
                return self.get_response(request)

            # Otherwise, show maintenance page with HTTP 503
            return render(request, 'stores/maintenance.html', status=503)

        # If not in maintenance mode, proceed normally
        return self.get_response(request)
