# Generated by Django 4.2.1 on 2023-06-09 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epoc_app', '0008_remove_patient_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]