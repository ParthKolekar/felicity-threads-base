# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_question_question_answer_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_score',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
    ]
