# Generated by Django 3.1.7 on 2021-04-27 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0008_leagueadmin'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LeagueAdmin',
        ),
        migrations.AlterModelOptions(
            name='league',
            options={'permissions': (('league_admin', 'Has league admin permissions'),)},
        ),
    ]
