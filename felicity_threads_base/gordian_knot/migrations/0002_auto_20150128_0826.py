# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gordian_knot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submission_string',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
