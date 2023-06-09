# Generated by Django 4.2.1 on 2023-06-08 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epoc_app', '0006_p_command_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('spo2', models.FloatField()),
                ('flow', models.FloatField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='T_Vs_t',
        ),
        migrations.RenameField(
            model_name='p_command',
            old_name='oxygenflow',
            new_name='flow',
        ),
        migrations.RenameField(
            model_name='p_info',
            old_name='humidity',
            new_name='spo2',
        ),
        migrations.RemoveField(
            model_name='p_info',
            name='temperature',
        ),
    ]
