# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import cuser.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(default=b'new', help_text=b'document status', max_length=50, choices=[(b'new', b'New'), (b'in_progress', b'In Progress'), (b'rejected', b'Rejected'), (b'approved', b'Approved'), (b'paid', b'Paid')])),
                ('created_by', cuser.fields.CurrentUserField(related_name='document_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DocumentStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('step_number', models.SmallIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('created_by', cuser.fields.CurrentUserField(related_name='documentstep_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('editors_group', models.ForeignKey(related_name='editors_group', to='auth.Group')),
                ('members_group', models.ForeignKey(related_name='members_group', to='auth.Group')),
                ('updated_by', cuser.fields.CurrentUserField(related_name='documentstep_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('viewers_group', models.ForeignKey(related_name='viewers_group', to='auth.Group')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DocumentTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('created_by', cuser.fields.CurrentUserField(related_name='documenttemplate_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('creators_group', models.ForeignKey(related_name='group_creators', to='auth.Group')),
                ('owner', models.ForeignKey(related_name='document_owner', to=settings.AUTH_USER_MODEL)),
                ('updated_by', cuser.fields.CurrentUserField(related_name='documenttemplate_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DocumentTemplateField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('widget', models.CharField(default=b'string', help_text=b'field widget', max_length=50, choices=[(b'string', b'String'), (b'text', b'TEXT'), (b'calculated', b'Calculated Field')])),
                ('created_by', cuser.fields.CurrentUserField(related_name='documenttemplatefield_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('template', models.ForeignKey(related_name='document_template', to='documents.DocumentTemplate')),
                ('updated_by', cuser.fields.CurrentUserField(related_name='documenttemplatefield_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DocumentValues',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.TextField(default=b'', null=True, blank=True)),
                ('created_by', cuser.fields.CurrentUserField(related_name='documentvalues_created_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('document', models.ForeignKey(related_name='document', to='documents.Document')),
                ('field', models.ForeignKey(related_name='document_field', to='documents.DocumentTemplateField')),
                ('updated_by', cuser.fields.CurrentUserField(related_name='documentvalues_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='document',
            name='step',
            field=models.ForeignKey(related_name='document_step', to='documents.DocumentStep'),
        ),
        migrations.AddField(
            model_name='document',
            name='updated_by',
            field=cuser.fields.CurrentUserField(related_name='document_updated_by', default=b'', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
