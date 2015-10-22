# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0006_auto_20151022_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='share_flag',
            field=models.BooleanField(default=0, choices=[(0, b'No'), (1, b'Yes')]),
        ),
    ]
