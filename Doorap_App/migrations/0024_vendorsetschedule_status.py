# Generated by Django 4.0.4 on 2022-05-24 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0023_alter_venderservices_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorsetschedule',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
