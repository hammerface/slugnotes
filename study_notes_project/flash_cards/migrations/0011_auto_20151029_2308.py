# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0010_auto_20151026_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_name',
            field=models.CharField(max_length=35),
        ),
    ]
