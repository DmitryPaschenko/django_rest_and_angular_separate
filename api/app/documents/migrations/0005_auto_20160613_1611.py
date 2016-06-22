# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_remove_documenttemplate_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documenttemplatestep',
            name='editors_group',
        ),
        migrations.RemoveField(
            model_name='documenttemplatestep',
            name='viewers_group',
        ),
        migrations.AddField(
            model_name='documenttemplatestep',
            name='editable_fields',
            field=models.ManyToManyField(related_name='editable_fields', to='documents.DocumentTemplateField', blank=True),
        ),
        migrations.AddField(
            model_name='documenttemplatestep',
            name='readonly_fields',
            field=models.ManyToManyField(related_name='readonly_fields', to='documents.DocumentTemplateField', blank=True),
        ),
    ]
