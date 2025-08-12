from django.contrib.auth.decorators import user_passes_test, login_required

def in_brian_group(user):
    return user.is_authenticated and user.groups.filter(name='Brian').exists()

def brian_login_required(view_func):
    decorated_view_func = login_required(view_func, login_url='/office/login/')
    return user_passes_test(in_brian_group, login_url='/office/login/')(decorated_view_func)
