import os

from django.test import TestCase


class TestEnvironmentSettings(TestCase):
    def test_django_setting_module(self):
        self.assertEqual(os.environ.get('DJANGO_SETTINGS_MODULE'), 'ecommerce.settings',
                         "DJANGO_SETTINGS_MODULE is not set correctly.")
