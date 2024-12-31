from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce.accounts'

    def ready(self):
        import ecommerce.accounts.signals
