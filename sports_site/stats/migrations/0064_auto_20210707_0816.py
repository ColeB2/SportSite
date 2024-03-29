# Generated by Django 3.1.7 on 2021-07-07 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0063_auto_20210624_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='complete_games',
            new_name='complete_game',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='games',
            new_name='game',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='games_started',
            new_name='game_started',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='losses',
            new_name='loss',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='save_ops',
            new_name='save_op',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='shutouts',
            new_name='shutout',
        ),
        migrations.RenameField(
            model_name='playerpitchinggamestats',
            old_name='wins',
            new_name='win',
        ),
        migrations.RemoveField(
            model_name='playerpitchinggamestats',
            name='saves',
        ),
    ]
