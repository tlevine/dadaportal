# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('hit', models.BigIntegerField(serialize=False, primary_key=True)),
                ('session', models.BigIntegerField()),
                ('datetime_start', models.DateTimeField(default=datetime.datetime.now)),
                ('endpoint', models.TextField()),
                ('ip_address', models.IPAddressField()),
                ('user_agent', models.TextField()),
                ('referrer', models.URLField()),
                ('status_code', models.SmallIntegerField(null=True)),
                ('datetime_end', models.DateTimeField(null=True)),
                ('availWidth', models.IntegerField(null=True)),
                ('availHeight', models.IntegerField(null=True)),
                ('scrollMaxX', models.IntegerField(null=True)),
                ('scrollMaxY', models.IntegerField(null=True)),
                ('pageXOffset', models.IntegerField(null=True)),
                ('pageYOffset', models.IntegerField(null=True)),
                ('javascript_enabled', models.NullBooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
