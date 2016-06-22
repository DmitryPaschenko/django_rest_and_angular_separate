# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('documents', '0002_documenttemplate_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTemplateStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('step_number', models.SmallIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('created_by', cuser.fields.CurrentUserField(related_name='documenttemplatestep_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('editors_group', models.ForeignKey(related_name='editors_group', to='auth.Group')),
                ('members_group', models.ForeignKey(related_name='members_group', to='auth.Group')),
                ('template', models.ForeignKey(related_name='document_template_steps', to='documents.DocumentTemplate')),
                ('updated_by', cuser.fields.CurrentUserField(related_name='documenttemplatestep_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('viewers_group', models.ForeignKey(related_name='viewers_group', to='auth.Group')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='documentstep',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='documentstep',
            name='editors_group',
        ),
        migrations.RemoveField(
            model_name='documentstep',
            name='members_group',
        ),
        migrations.RemoveField(
            model_name='documentstep',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='documentstep',
            name='viewers_group',
        ),
        migrations.AlterField(
            model_name='document',
            name='step',
            field=models.ForeignKey(related_name='document_step', to='documents.DocumentTemplateStep'),
        ),
        migrations.AlterField(
            model_name='documenttemplatefield',
            name='template',
            field=models.ForeignKey(related_name='document_template_fields', to='documents.DocumentTemplate'),
        ),
        migrations.DeleteModel(
            name='DocumentStep',
        ),
    ]
