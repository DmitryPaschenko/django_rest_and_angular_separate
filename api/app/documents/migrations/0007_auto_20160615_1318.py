# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20160614_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentvalues',
            name='document',
            field=models.ForeignKey(related_name='document_values', to='documents.Document'),
        ),
    ]
