# Generated by Django 2.1rc1 on 2019-08-08 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OftyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badass', models.BooleanField(default=False)),
                ('enable_push', models.BooleanField(default=True)),
                ('enable_sound_alert', models.BooleanField(default=True)),
                ('enable_sms_new_order', models.BooleanField(default=True)),
                ('enable_sms_startstop', models.BooleanField(default=True)),
                ('enable_email_new_order', models.BooleanField(default=True)),
                ('enable_email_startstop', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]