# Generated by Django 2.2.6 on 2019-12-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20190814_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='oftyuserrentlord',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='oftyuserrentlord',
            name='site',
            field=models.URLField(default=''),
        ),
    ]