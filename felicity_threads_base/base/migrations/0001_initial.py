# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_title', models.CharField(unique=True, max_length=255)),
                ('question_desc', models.TextField()),
                ('question_image', models.ImageField(upload_to=base.models.question_image_filepath)),
                ('question_level', models.IntegerField()),
                ('question_level_id', models.IntegerField()),
                ('question_upload_type', models.CharField(default=b'ST', max_length=2, choices=[(b'FL', b'File'), (b'ST', b'String')])),
                ('question_upload_file', models.FileField(upload_to=b'')),
                ('question_checker_script', models.FileField(upload_to=base.models.question_checker_script)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_timestamp', models.DateField(auto_now=True, auto_now_add=True)),
                ('submission_question', models.ForeignKey(to='base.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_name', models.CharField(max_length=255)),
                ('team_score', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_username', models.CharField(max_length=255)),
                ('user_email', models.EmailField(unique=True, max_length=255)),
                ('user_nick', models.CharField(max_length=255)),
                ('user_firstname', models.CharField(max_length=255)),
                ('user_surname', models.CharField(max_length=255)),
                ('user_country', models.CharField(max_length=10)),
                ('user_location', models.CharField(max_length=255)),
                ('user_last_ip', models.GenericIPAddressField(editable=False)),
                ('user_timestamp', models.DateField(auto_now=True, auto_now_add=True)),
                ('user_access_level', models.IntegerField(default=1, editable=False)),
                ('user_team', models.ForeignKey(to='base.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_user',
            field=models.ForeignKey(to='base.User'),
            preserve_default=True,
        ),
    ]
