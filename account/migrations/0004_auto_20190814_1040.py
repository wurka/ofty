# Generated by Django 2.1rc1 on 2019-08-14 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20190812_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='oftyuser',
            name='money',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='stock_size',
            field=models.IntegerField(default=10),
        ),
    ]