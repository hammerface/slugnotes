# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0002_auto_20151018_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='deck_name',
            field=models.CharField(default=b'Untitled Deck', max_length=100),
        ),
    ]
