# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0005_auto_20151018_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_id',
            field=models.AutoField(serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='deleted_flag',
            field=models.BooleanField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='deck',
            name='deck_id',
            field=models.AutoField(serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='deck',
            name='deck_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='deck',
            name='deleted_flag',
            field=models.BooleanField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='deck',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
