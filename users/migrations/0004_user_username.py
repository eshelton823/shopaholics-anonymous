# Generated by Django 2.2.5 on 2019-10-20 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191020_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]