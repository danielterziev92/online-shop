import os
import time

import dramatiq
from django.core.cache import cache
from django.db import connection
from environ import Env

from ecommerce.settings import BASE_DIR
from tests.base import AppTestCase


@dramatiq.actor
def test_cache(key, value):
    cache.set(key, value, timeout=2)


class Connection(AppTestCase):
    def test_database_connection(self):
        env = Env()
        env.read_env(os.path.join(BASE_DIR, '.env'))

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')

            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Database connection failed: {e}")

    def test_redis_connection(self):
        key = 'my_key'
        value = 'my_value'

        cache.set(key, value, timeout=1)

        cache_value = cache.get(key)
        self.assertEqual(value, cache_value)

        time.sleep(1.2)

        cache_value = cache.get(key)
        self.assertIsNone(cache_value)

    def test_dramatiq_task_execution(self):
        key = 'test_key'
        value = 'test_value'

        test_cache(key=key, value=value)

        time.sleep(1)

        result = cache.get(key)
        self.assertEqual(result, value)
