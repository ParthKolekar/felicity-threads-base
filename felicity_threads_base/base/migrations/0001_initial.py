# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_username', models.CharField(max_length=255)),
                ('user_email', models.EmailField(unique=True, max_length=255)),
                ('user_nick', models.CharField(max_length=255)),
                ('user_last_ip', models.GenericIPAddressField()),
                ('user_timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('user_access_level', models.IntegerField(default=1, editable=False)),
                ('user_score', models.FloatField(default=0, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
