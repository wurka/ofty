# Generated by Django 3.0.2 on 2020-01-24 07:56

import datetime
from django.db import migrations, models
import pytz


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20191207_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='oftyuser',
            name='verification_code',
            field=models.BinaryField(default=b''),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='verification_code_until',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC)),
        ),
    ]
