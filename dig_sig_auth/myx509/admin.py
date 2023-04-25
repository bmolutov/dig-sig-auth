from django.contrib import admin
from swapper import load_model

from django_x509.base.admin import AbstractCaAdmin, AbstractCertAdmin


Ca = load_model('django_x509', 'Ca')
Cert = load_model('django_x509', 'Cert')


class CertAdmin(AbstractCertAdmin):
    # add your changes here
    pass


class CaAdmin(AbstractCaAdmin):
    # add your changes here
    pass


admin.site.register(Ca, CaAdmin)
admin.site.register(Cert, CertAdmin)
