# Generated by Django 2.2.7 on 2019-11-22 14:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_auto_20191119_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
