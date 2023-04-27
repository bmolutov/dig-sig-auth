import base64

from django.http import HttpResponse
from cryptography.hazmat.primitives import serialization
from django.shortcuts import render, redirect

from .backends import CertificateAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.shortcuts import render

from .forms import RegistrationForm, CertificateLoginForm, BasicAuthLoginForm
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
    authentication_classes = [CertificateAuthentication]

    def post(self, request, *args, **kwargs):
        backend = CertificateAuthentication()
        user = backend.authenticate(self.request)
        if user is not None:
            return Response({'username': user[0].username, 'message': 'success'})
        else:
            return Response({'error': 'Invalid certificate'})


def home(request):
    context = {
        'message': 'Hello, World!'
    }
    return render(request, 'home.html', context)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # create user
            user = User()
            user.username = username
            user.password = password
            user.save()

            # return redirect('registration_success', username=username)
            request.session['username'] = username
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


def certificate_login(request):
    if request.method == 'POST':
        form = CertificateLoginForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            certificate = form.cleaned_data['certificate']

            backend = CertificateAuthentication()
            user = backend.authenticate(request)
            if user is not None:
                request.session['username'] = user[0].username
                return redirect('certificate_login_success')
            else:
                return Response({'error': 'Invalid certificate'})

    else:
        form = CertificateLoginForm()
    return render(request, 'certificate_login/certificate_login.html', {'form': form})


def basic_auth_login(request):
    if request.method == 'POST':
        form = BasicAuthLoginForm(request, data=request.POST)
        if form.is_valid():
            # todo: complete
            return redirect('basic_auth_login_success')
    else:
        form = BasicAuthLoginForm(request)
    return render(request, 'basic_auth_login/basic_auth_login.html', {'form': form})


def registration_success(request, **kwargs):
    username = request.session.get('username')

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


def certificate_login_success(request):
    context = {'username': request.session.get('username')}
    return render(request, 'certificate_login/certificate_login_success.html', context)


def basic_auth_login_success(request):
    return render(request, 'basic_auth_login/basic_auth_login_success.html')
