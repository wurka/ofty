# Generated by Django 3.0.4 on 2020-03-25 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200204_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='oftyuser',
            name='new_deals',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='new_messages',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='new_orders',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='oftyuser',
            name='units_in_basket',
            field=models.IntegerField(default=0),
        ),
    ]
