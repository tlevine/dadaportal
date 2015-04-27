# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_auto_20150425_2210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hit',
            old_name='scrollMaxX',
            new_name='scrollX',
        ),
        migrations.RenameField(
            model_name='hit',
            old_name='scrollMaxY',
            new_name='scrollY',
        ),
        migrations.AlterField(
            model_name='hit',
            name='ip_address',
            field=models.GenericIPAddressField(),
        ),
    ]
