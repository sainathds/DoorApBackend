# Generated by Django 4.0.4 on 2022-06-06 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0037_offers'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommisionMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commision', models.FloatField(blank=True, null=True)),
                ('user_type', models.CharField(blank=True, max_length=200, null=True)),
                ('fk_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.categorymaster')),
                ('fk_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.countrymaster')),
            ],
        ),
    ]
