# Generated by Django 4.0.4 on 2022-06-16 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0047_orderdetails_vendor_pay_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='fk_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.countrymaster'),
        ),
    ]
