# Generated by Django 4.0.4 on 2022-06-20 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamehundred', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='user',
        ),
    ]
