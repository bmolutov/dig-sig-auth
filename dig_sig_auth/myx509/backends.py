from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from cryptography import x509
from cryptography.hazmat.backends import default_backend


class CertificateAuthentication(BaseBackend, BaseAuthentication):
    def authenticate(self, request, **kwargs):
        # Get the certificate from the request
        certificate = request.FILES.get('certificate')
        # certificate = request.META.get('HTTP_X_SSL_CLIENT_CERT')

        if not certificate:
            # If the certificate is not provided, raise an authentication failed error
            raise AuthenticationFailed('No client certificate found.')

        try:
            # Load the certificate from the file object
            certificate = x509.load_pem_x509_certificate(certificate.read(), default_backend())

            # Extract the common name from the certificate
            common_name = certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

            # Use the CN to look up the user in the database
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(username=common_name)
            except UserModel.DoesNotExist:
                raise AuthenticationFailed('User not found.')

            # Return the user and None (authentication successful)
            return user, None

        except Exception as e:
            # If there is an error parsing or validating the certificate, raise an authentication failed error
            print(e)
            raise AuthenticationFailed('Invalid client certificate.')

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:  # noqa
            return None

    def authenticate_header(self, request):
        return 'Basic realm="My Realm"'
