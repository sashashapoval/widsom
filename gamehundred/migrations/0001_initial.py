# Generated by Django 4.0.4 on 2022-06-20 14:14

from django.db import migrations, models
import gamehundred.game_of_hundred


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal', models.IntegerField(default=100, help_text='Enter the number the players must reach')),
                ('rules', models.TextField(blank=True, help_text='Enter a brief description of the game', max_length=10000)),
                ('number_cur', models.IntegerField(default=0, help_text='The number at which the players start')),
                ('number_max_avail', models.IntegerField(default=10, help_text='The number at which the players start')),
                ('number_magic', models.IntegerField(default=11, help_text='The number at which the players start')),
                ('user', models.ManyToManyField(help_text='User', to='gamehundred.user')),
            ],
            bases=(models.Model, gamehundred.game_of_hundred.game_of_one_hundred),
        ),
    ]