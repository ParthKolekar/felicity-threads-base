# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20150104_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
