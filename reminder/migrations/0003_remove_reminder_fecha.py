# Generated by Django 4.1.7 on 2023-05-09 05:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0002_alter_reminder_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='fecha',
        ),
    ]
