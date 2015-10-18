# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('deck_id', models.AutoField(serialize=False, primary_key=True)),
                ('deck_name', models.CharField(max_length=100)),
                ('share_flag', models.BooleanField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('deleted_flag', models.BooleanField(default=0)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
