from django.http import HttpResponse
from cryptography.hazmat.primitives import serialization
from .backends import CertificateAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Cert, Ca


@extend_schema(
    operation_id='upload_file',
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'certificate': {
                    'type': 'string',
                    'format': 'binary'
                }
            }
        }
    },
)
class CertificateAuthenticationView(APIView):
    def post(self, request, *args, **kwargs):
        backend = CertificateAuthentication()
        user = backend.authenticate(self.request)
        if user is not None:
            return Response({'username': user[0].username, 'message': 'success'})
        else:
            return Response({'error': 'Invalid certificate'})


@extend_schema(
    parameters=[
        OpenApiParameter(name='password', description='client password', required=True, type=str),
        OpenApiParameter(name='username', description='client username', required=True, type=str),
    ]
)
class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        username = self.request.query_params.get('username')
        password = self.request.query_params.get('password')

        # create user
        user = User()
        user.username = username
        user.password = password
        user.save()

        # create certificate for the user
        certificate = Cert()
        certificate.ca = Ca.objects.get(name='test-ca-1')  # noqa
        certificate.name = username
        certificate.common_name = username
        certificate.save()

        x509 = certificate.x509
        # Convert the X509 object to bytes
        cert_bytes = x509.to_cryptography().public_bytes(encoding=serialization.Encoding.PEM)

        # Create the HTTP response with the certificate data
        response = HttpResponse(cert_bytes, content_type='application/x-x509-ca-cert')
        response['Content-Disposition'] = 'attachment; filename="certificate.pem"'

        return response
