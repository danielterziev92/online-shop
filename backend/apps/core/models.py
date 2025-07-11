from django.db import models

from utilities.models import TimeStampModel


class ConfigurationSettingBase(TimeStampModel):
    KEY_MAX_LENGTH = 255

    key = models.CharField(
        max_length=KEY_MAX_LENGTH,
        null=False,
        blank=False,
    )

    value = models.JSONField(
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True


class ConfigurationSetting(ConfigurationSettingBase):
    class Meta:
        db_table = "configuration_settings"
        constraints = (
            models.UniqueConstraint(fields=("key",), name="unique_config_key"),
        )

# class AccountConfigurationSetting(ConfigurationSettingBase):
#     account = models.ForeignKey(
#         to=AccountModel,
#         on_delete=models.CASCADE,
#         related_name="configuration_settings"
#     )
#
#     class Meta:
#         db_table = "account_configuration_settings"
#         constraints = (
#             models.UniqueConstraint(fields=("key", "account"), name="unique_account_config_key"),
#         )
