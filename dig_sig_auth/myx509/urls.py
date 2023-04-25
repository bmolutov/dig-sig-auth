from django.urls import path
from .views import CertificateAuthenticationView, RegistrationView


urlpatterns = [
    path('authenticate/', CertificateAuthenticationView.as_view(), name='certificate-authentication'),
    path('register/', RegistrationView.as_view(), name='certificate-registration'),
]
