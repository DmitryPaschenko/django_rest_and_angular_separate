# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20160603_0912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documenttemplate',
            name='owner',
        ),
    ]
