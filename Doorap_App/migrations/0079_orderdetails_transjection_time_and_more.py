# Generated by Django 4.0.4 on 2022-07-21 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0078_rename_token_orderdetails_stripe_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='transjection_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='transjection_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
