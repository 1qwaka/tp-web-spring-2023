# Generated by Django 4.2 on 2023-05-23 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='registration_date',
        ),
    ]