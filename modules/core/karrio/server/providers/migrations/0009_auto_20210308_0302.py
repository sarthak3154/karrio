# Generated by Django 3.1.7 on 2021-03-08 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0008_auto_20210214_0409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrier',
            old_name='user',
            new_name='created_by',
        ),
    ]