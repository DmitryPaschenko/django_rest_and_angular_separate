# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20160615_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentvalues',
            name='value',
        ),
        migrations.AddField(
            model_name='documenttemplatefield',
            name='widget_metadata',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='documentvalues',
            name='_value',
            field=models.TextField(default=b'', null=True, db_column=b'value', blank=True),
        ),
        migrations.AlterField(
            model_name='documenttemplatefield',
            name='widget',
            field=models.CharField(default=b'string', help_text=b'field widget', max_length=50, choices=[(b'date', b'Date'), (b'number', b'Number'), (b'select', b'Select'), (b'string', b'String'), (b'text', b'Text'), (b'calculated', b'Calculated Field')]),
        ),
    ]
