# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FishQuery',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('location', models.CharField(max_length=200)),
                ('location_id', models.IntegerField()),
                ('species', models.CharField(max_length=200)),
                ('species_id', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
    ]
