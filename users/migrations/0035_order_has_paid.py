# Generated by Django 2.2.5 on 2019-11-17 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20191117_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
    ]