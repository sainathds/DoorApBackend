# Generated by Django 4.0.4 on 2022-07-25 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0081_rename_customer_id_orderdetails_payment_intent_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetails',
            old_name='stripe_token',
            new_name='stripe_refund_txtid',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='stripe_refund_link',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='stripe_txn_status',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='transjection_date',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='transjection_id',
        ),
        migrations.RemoveField(
            model_name='orderdetails',
            name='transjection_time',
        ),
    ]
