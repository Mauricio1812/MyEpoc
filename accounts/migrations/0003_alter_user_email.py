# Generated by Django 4.2.1 on 2023-10-02 21:25

from django.db import migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=encrypted_fields.fields.EncryptedEmailField(max_length=256),
        ),
    ]