# Generated by Django 4.0.4 on 2022-06-17 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doorap_App', '0050_alter_addtocart_hour'),
    ]

    operations = [
        migrations.AddField(
            model_name='likedislike',
            name='fk_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Doorap_App.categorymaster'),
        ),
    ]
