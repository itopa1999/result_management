# Generated by Django 4.2.3 on 2023-08-03 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_historicaluser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalUser',
        ),
    ]