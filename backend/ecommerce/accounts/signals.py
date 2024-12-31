from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce.accounts.models import AccountVerification, BaseAccount
from ecommerce.accounts.tasks import send_verification_email


@receiver(post_save, sender=BaseAccount)
def create_verification_code(sender, instance, created, **kwargs):
    if not created:
        return

    verification = AccountVerification.objects.create(account=instance)
    send_verification_email.send(instance.email, verification.verification_code)
