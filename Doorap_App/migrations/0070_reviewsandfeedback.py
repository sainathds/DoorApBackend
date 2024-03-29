# Generated by Django 4.0.4 on 2022-07-14 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0069_rename_booking_time_orderdetails_current_booking_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewsandFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('is_feedback', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=False)),
                ('fk_orderdetails', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.orderdetails')),
                ('fk_vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.vendordetails')),
            ],
        ),
    ]
