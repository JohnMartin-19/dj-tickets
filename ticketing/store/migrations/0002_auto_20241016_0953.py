# Generated by Django 3.2.18 on 2024-10-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='price',
        ),
        migrations.AddField(
            model_name='ticket',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
