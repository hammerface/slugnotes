# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0004_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='deck_id',
            new_name='deck',
        ),
    ]
