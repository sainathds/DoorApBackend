# Generated by Django 4.0.4 on 2022-05-14 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0012_remove_myuser_password1_remove_myuser_password2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendordetails',
            name='google_address_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendordetails',
            name='google_address_lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
