# Generated by Django 4.2.1 on 2023-10-02 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_room_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('attended', 'Attended'), ('waiting', 'Waiting')], default='waiting', max_length=20),
        ),
    ]
