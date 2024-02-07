# Generated by Django 4.2.3 on 2023-08-03 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_tracking_historicaltracking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaloutstanding',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpayment',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpayment',
            name='student',
        ),
        migrations.RemoveField(
            model_name='historicalresult',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltracking',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalGPA',
        ),
        migrations.DeleteModel(
            name='HistoricalOutstanding',
        ),
        migrations.DeleteModel(
            name='HistoricalPayment',
        ),
        migrations.DeleteModel(
            name='HistoricalResult',
        ),
        migrations.DeleteModel(
            name='HistoricalTracking',
        ),
    ]
