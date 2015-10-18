# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0003_auto_20151018_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_id', models.AutoField(serialize=False, primary_key=True)),
                ('front', models.CharField(max_length=1000)),
                ('back', models.CharField(max_length=2000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('deleted_flag', models.BooleanField(default=0)),
                ('deck_id', models.ForeignKey(to='flash_cards.Deck')),
            ],
        ),
    ]
