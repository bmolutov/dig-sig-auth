# from django.apps import AppConfig
#
#
# class Myx509Config(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'myx509'

from django_x509.apps import DjangoX509Config


class Myx509Config(DjangoX509Config):
    name = 'myx509'
    verbose_name = 'myx509'
