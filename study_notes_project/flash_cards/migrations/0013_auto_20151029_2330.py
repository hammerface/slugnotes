# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0012_auto_20151029_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='back',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='card',
            name='front',
            field=models.CharField(max_length=1000),
        ),
    ]
