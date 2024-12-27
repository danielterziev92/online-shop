import os

from django.db import connection
from environ import Env

from ecommerce.settings import BASE_DIR
from tests.base import AppTestCase


class TestDatabaseConnection(AppTestCase):
    def test_database_connection(self):
        env = Env()
        env.read_env(os.path.join(BASE_DIR, '.env'))

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')

            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
