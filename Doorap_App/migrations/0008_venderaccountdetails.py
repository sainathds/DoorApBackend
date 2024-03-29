# Generated by Django 4.0.4 on 2022-05-09 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0007_alter_myuser_created_datime'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenderAccountDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(blank=True, max_length=200, null=True)),
                ('account_no', models.CharField(blank=True, max_length=200, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=100, null=True)),
                ('account_status', models.BooleanField(default=False)),
                ('fk_vender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.vendordetails')),
            ],
        ),
    ]
