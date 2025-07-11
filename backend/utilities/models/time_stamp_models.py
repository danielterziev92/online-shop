from django.db import models


class CreateTimeStampModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True


class UpdateTimeStampModel(models.Model):
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class TimeStampModel(CreateTimeStampModel, UpdateTimeStampModel):
    class Meta:
        abstract = True
