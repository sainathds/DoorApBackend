# Generated by Django 4.0.4 on 2022-06-15 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0043_orderdetails_fk_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='order_status',
        ),
        migrations.AddField(
            model_name='orderservice',
            name='order_status',
            field=models.CharField(default='Pending', max_length=200),
        ),
    ]
