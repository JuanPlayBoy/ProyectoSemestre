# Generated by Django 4.1.7 on 2023-03-24 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='fechaLim',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
