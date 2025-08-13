from django.conf import settings
from django.shortcuts import render

class MaintenanceModeMiddleware:
    ALLOWED_USERS = {'pccballard'}  # Add more usernames if needed

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check maintenance mode from settings
        if getattr(settings, 'SITE_MAINTENANCE_MODE', False):
            # 
            # Skip admin, office, static, and media URLs
            if request.path.startswith('/admin/') or request.path.startswith('/office/') or request.path.startswith(settings.STATIC_URL) or request.path.startswith('/media/'):
                return self.get_response(request)

            # Allow API requests
            if request.path.startswith('/orders/api/'):
                return self.get_response(request)

            # Allow staff/admin users
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)

            # Allow specific allowed usernames
            if request.user.is_authenticated and request.user.username in self.ALLOWED_USERS:
                return self.get_response(request)

            # Allow login page
            if request.path == '/accounts/login/':
                return self.get_response(request)

            # Otherwise, show maintenance page
            return render(request, 'stores/maintenance.html', status=503)

        # Normal processing if not in maintenance mode
        return self.get_response(request)

# from django.conf import settings
# from django.shortcuts import render
# from django.urls import resolve, Resolver404

# class MaintenanceModeMiddleware:
#     ALLOWED_USERS = {'pccballard'}  # Add more usernames if needed

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if getattr(settings, 'SITE_MAINTENANCE_MODE', False):
#             # Allow API requests
#             if request.path.startswith('/orders/api/'):
#                 return self.get_response(request)

#             # Allow static and media files (optional, adjust paths as needed)
#             if request.path.startswith(settings.STATIC_URL) or request.path.startswith('/media/'):
#                 return self.get_response(request)

#             # Allow staff/admin users
#             if request.user.is_authenticated and request.user.is_staff:
#                 return self.get_response(request)

#             # Allow specific allowed usernames
#             if request.user.is_authenticated and request.user.username in self.ALLOWED_USERS:
#                 return self.get_response(request)

#             # Allow login and admin login pages
#             try:
#                 url_name = resolve(request.path_info).url_name
#             except Resolver404:
#                 url_name = None

#             if url_name in ['login', 'admin:login']:
#                 return self.get_response(request)

#             # Otherwise, show maintenance page with HTTP 503
#             return render(request, 'stores/maintenance.html', status=503)

#         # If not in maintenance mode, proceed normally
#         return self.get_response(request)
