# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('comment_message', models.CharField(default=b'', max_length=255)),
                ('comment_is_approved', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_level', models.IntegerField()),
                ('question_level_id', models.IntegerField()),
                ('question_title', models.CharField(unique=True, max_length=255)),
                ('question_desc', models.TextField()),
                ('question_image', models.ImageField(upload_to=base.models.question_image_filepath, blank=True)),
                ('question_upload_type', models.CharField(default=b'ST', max_length=2, choices=[(b'FL', b'File'), (b'ST', b'String')])),
                ('question_answer_string', models.CharField(default=b'', max_length=255, blank=True)),
                ('question_upload_file', models.FileField(upload_to=base.models.question_file_upload, blank=True)),
                ('question_checker_script', models.FileField(upload_to=base.models.question_checker_upload, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('submission_string', models.CharField(default=b'', max_length=255)),
                ('submission_storage', models.FileField(upload_to=base.models.submission_storage_path)),
                ('submission_state', models.CharField(default=b'PR', max_length=2, choices=[(b'WA', b'Wrong Answer'), (b'AC', b'Accepted'), (b'PR', b'Processing')])),
                ('submission_score', models.FloatField(default=0)),
                ('submission_question', models.ForeignKey(to='gordion_knot.Question')),
                ('submission_user', models.ForeignKey(related_name='gordion_knot_submission_related', to='base.User')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_question',
            field=models.ForeignKey(to='gordion_knot.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(to='base.User'),
            preserve_default=True,
        ),
    ]
