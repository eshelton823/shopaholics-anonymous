# Generated by Django 2.2.5 on 2019-10-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20191024_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='has_order',
            field=models.BooleanField(default=False),
        ),
    ]
