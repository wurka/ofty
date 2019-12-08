# Generated by Django 2.2.1 on 2019-12-07 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20191202_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_email_new_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_email_startstop',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_push',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_sms_new_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_sms_startstop',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='enable_sound_alert',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='phone',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='oftyuser',
            name='phone2',
            field=models.TextField(default=''),
        ),
    ]
