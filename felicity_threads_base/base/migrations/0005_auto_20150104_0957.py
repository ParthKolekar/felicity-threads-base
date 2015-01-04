# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_submission_submission_storage'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submission_state',
            field=models.CharField(default=b'PR', max_length=2, choices=[(b'WA', b'Wrong Answer'), (b'AC', b'Accepted'), (b'PR', b'Processing')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='question_checker_script',
            field=models.FileField(upload_to=base.models.question_checker_script, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='question_image',
            field=models.ImageField(upload_to=base.models.question_image_filepath, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='question_upload_file',
            field=models.FileField(upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
