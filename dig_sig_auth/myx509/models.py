from django.db import models
from django_x509.base.models import AbstractCa, AbstractCert


class DetailsModel(models.Model):
    details = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        abstract = True


class Ca(DetailsModel, AbstractCa):
    """
    Concrete Ca model
    """
    class Meta(AbstractCa.Meta):
        abstract = False


class Cert(DetailsModel, AbstractCert):
    """
    Concrete Cert model
    """
    name = models.CharField(max_length=64, unique=True, verbose_name='username')
    common_name = models.CharField('common name', max_length=64, blank=True, unique=True)

    class Meta(AbstractCert.Meta):
        abstract = False
