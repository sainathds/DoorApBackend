# Generated by Django 4.0.4 on 2022-06-22 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0052_offers_expirydate_offers_offercode_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='used_promocode',
            field=models.IntegerField(default=0),
        ),
    ]
