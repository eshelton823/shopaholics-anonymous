# Generated by Django 2.2.7 on 2019-11-11 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_auto_20191110_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='chat_room',
            field=models.CharField(default="", max_length=32),
            preserve_default=False,
        ),
    ]
