# from django_x509.tests.base import TestX509Mixin
from django_x509.tests.test_admin import ModelAdminTests as BaseModelAdminTests
from django_x509.tests.test_ca import TestCa as BaseTestCa
from django_x509.tests.test_cert import TestCert as BaseTestCert


class ModelAdminTests(BaseModelAdminTests):
    app_label = 'myx509'


class TestCert(BaseTestCert):
    pass


class TestCa(BaseTestCa):
    pass


del BaseModelAdminTests
del BaseTestCa
del BaseTestCert
