# Generated by Django 2.2.5 on 2019-11-10 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_auto_20191110_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]
