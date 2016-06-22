# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20160613_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documenttemplatestep',
            options={'ordering': ['step_number']},
        ),
        migrations.AddField(
            model_name='document',
            name='template',
            field=models.ForeignKey(related_name='document_templates', default='', to='documents.DocumentTemplate'),
            preserve_default=False,
        ),
    ]
