# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20150104_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submission_storage',
            field=models.FileField(default=datetime.datetime(2015, 1, 4, 8, 57, 56, 668276, tzinfo=utc), upload_to=base.models.submission_storage_path, editable=False),
            preserve_default=False,
        ),
    ]
