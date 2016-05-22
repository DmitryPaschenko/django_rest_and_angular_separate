# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 22, 19, 58, 15, 999079, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='created_by',
            field=cuser.fields.CurrentUserField(related_name='appuser_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 22, 19, 58, 21, 151044, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appuser',
            name='updated_by',
            field=cuser.fields.CurrentUserField(related_name='appuser_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
