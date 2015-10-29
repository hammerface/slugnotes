# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0011_auto_20151029_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='back',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='card',
            name='front',
            field=models.TextField(max_length=1000),
        ),
    ]
