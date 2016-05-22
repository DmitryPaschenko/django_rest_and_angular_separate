from django.contrib.auth.models import AbstractUser
from django.db import models
from dp_base_libs.models import DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable


class AppUser(AbstractUser, DPAbstractModel, DPAbstractSignable, DPAbstractTimestampable):
    detailed_info = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(AppUser, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']




