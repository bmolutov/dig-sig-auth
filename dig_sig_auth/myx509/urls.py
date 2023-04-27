from .views import home
from django.urls import path
from .views import registration, certificate_login, basic_auth_login, \
    registration_success, certificate_login_success, basic_auth_login_success


urlpatterns = [
    path('', home, name='home'),

    path('registration/', registration, name='registration'),
    path('certificate-login/', certificate_login, name='certificate_login'),
    path('basic-auth-login/', basic_auth_login, name='basic_auth_login'),

    path('registration-success/', registration_success, name='registration_success'),
    path('certificate-login-success/', certificate_login_success, name='certificate_login_success'),
    path('basic-auth-login-success/', basic_auth_login_success, name='basic_auth_login_success'),

]
