# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_auto_20150427_1006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='referrer',
            field=models.URLField(max_length=10000),
        ),
    ]
