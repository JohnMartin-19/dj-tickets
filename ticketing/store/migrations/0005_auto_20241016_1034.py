# Generated by Django 3.2.18 on 2024-10-16 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20241016_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AddField(
            model_name='ticketitem',
            name='price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
