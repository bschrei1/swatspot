# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharples', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endTime', models.DateTimeField(verbose_name=b'time of last swipe in the interval')),
                ('startTime', models.DateTimeField(verbose_name=b'time of first swipe in the interval')),
                ('numUpdates', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
