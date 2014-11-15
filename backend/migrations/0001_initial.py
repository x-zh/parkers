# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=b'', max_length=5, blank=True)),
                ('status', models.CharField(default=b'', max_length=15, blank=True)),
                ('main_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('from_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('to_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('side', models.CharField(default=b'', max_length=5, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationWithLatLng',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=b'', max_length=5, blank=True)),
                ('status', models.CharField(default=b'', max_length=15, blank=True)),
                ('main_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('from_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('to_street', models.CharField(default=b'', max_length=255, blank=True)),
                ('side', models.CharField(default=b'', max_length=5, blank=True)),
                ('lat_main_from', models.DecimalField(default=0.0, max_digits=15, decimal_places=8)),
                ('lng_main_from', models.DecimalField(default=0.0, max_digits=15, decimal_places=8)),
                ('lat_main_to', models.DecimalField(default=0.0, max_digits=15, decimal_places=8)),
                ('lng_main_to', models.DecimalField(default=0.0, max_digits=15, decimal_places=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(default=b'', max_length=5, blank=True)),
                ('status', models.CharField(default=b'', max_length=15, blank=True)),
                ('sequence', models.IntegerField()),
                ('distance', models.IntegerField()),
                ('arrow', models.CharField(default=b'', max_length=5, blank=True)),
                ('description', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
