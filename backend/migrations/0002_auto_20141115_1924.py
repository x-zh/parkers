# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sign',
            name='code',
            field=models.CharField(default=b'', max_length=5, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sign',
            name='status',
            field=models.CharField(default=b'', max_length=15, db_index=True, blank=True),
        ),
    ]
