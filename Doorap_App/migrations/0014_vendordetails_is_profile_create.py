# Generated by Django 4.0.4 on 2022-05-17 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0013_alter_vendordetails_google_address_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendordetails',
            name='is_profile_create',
            field=models.BooleanField(default=False),
        ),
    ]
