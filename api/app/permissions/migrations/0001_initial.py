# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("INSERT INTO auth_permission(name, content_type_id, codename) VALUES ('Crm chief permission', 2, 'dp_crm_chief_permission');")
    ]
