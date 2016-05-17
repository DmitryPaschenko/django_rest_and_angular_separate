from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    detailed_info = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(AppUser, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']




