# Generated by Django 3.0.2 on 2020-02-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200124_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='oftyuser',
            name='negative',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='positive',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
