# Generated by Django 4.0.1 on 2022-03-22 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0030_alter_game_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['date', 'start_time']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]