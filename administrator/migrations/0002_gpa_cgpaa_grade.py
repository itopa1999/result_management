# Generated by Django 4.2.3 on 2023-08-02 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpa',
            name='cgpaa_grade',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]