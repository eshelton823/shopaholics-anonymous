# Generated by Django 2.2.5 on 2019-10-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191014_1917'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.AddField(
            model_name='order',
            name='driver',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='car_make',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='car_model',
            field=models.CharField(default='', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='deliveries_made',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='driver_filled',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_matching',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='license_identifier_number',
            field=models.CharField(default='', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='license_plate_number',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='money_earned',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='state_of_drivers_license_issuance',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]