# Generated by Django 2.2.5 on 2019-11-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_auto_20191119_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='past_driver',
            field=models.CharField(default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='past_user',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
