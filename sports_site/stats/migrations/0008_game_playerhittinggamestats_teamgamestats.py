# Generated by Django 3.1.7 on 2021-03-30 12:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stats', '0007_auto_20210329_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField(blank=True, default=datetime.time(19, 0), null=True, verbose_name='Time')),
                ('location', models.CharField(blank=True, help_text='Defaults to home team.', max_length=20, null=True)),
                ('stats_entered', models.BooleanField(default=False, null=True, verbose_name='Stats Entered')),
                ('final_score', models.CharField(blank=True, default='---', max_length=20, null=True)),
                ('away_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AwayTeam', to='stats.teamseason', verbose_name='Visitor')),
                ('home_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='HomeTeam', to='stats.teamseason', verbose_name='Home')),
                ('season', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.seasonstage')),
            ],
        ),
        migrations.CreateModel(
            name='TeamGameStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.game')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerHittingGameStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('at_bats', models.IntegerField(blank=True, default=0, null=True, verbose_name='AB')),
                ('plate_appearances', models.IntegerField(blank=True, default=0, null=True, verbose_name='PA')),
                ('hits', models.IntegerField(blank=True, default=0, null=True, verbose_name='H')),
                ('runs', models.IntegerField(blank=True, default=0, null=True, verbose_name='R')),
                ('strikeouts', models.IntegerField(blank=True, default=0, null=True, verbose_name='SO')),
                ('walks', models.IntegerField(blank=True, default=0, null=True, verbose_name='BB')),
                ('singles', models.IntegerField(blank=True, default=0, null=True, verbose_name='1B')),
                ('doubles', models.IntegerField(blank=True, default=0, null=True, verbose_name='2B')),
                ('triples', models.IntegerField(blank=True, default=0, null=True, verbose_name='3B')),
                ('homeruns', models.IntegerField(blank=True, default=0, null=True, verbose_name='HR')),
                ('stolen_bases', models.IntegerField(blank=True, default=0, null=True, verbose_name='SB')),
                ('caught_stealing', models.IntegerField(blank=True, default=0, null=True, verbose_name='CS')),
                ('runs_batted_in', models.IntegerField(blank=True, default=0, null=True, verbose_name='RBI')),
                ('hit_by_pitch', models.IntegerField(blank=True, default=0, null=True, verbose_name='HBP')),
                ('sacrifice_flies', models.IntegerField(blank=True, default=0, null=True, verbose_name='SF')),
                ('sacrifice_bunts', models.IntegerField(blank=True, default=0, null=True, verbose_name='SAC')),
                ('average', models.CharField(default='---', max_length=10, verbose_name='AVG')),
                ('on_base_percentage', models.CharField(default='---', max_length=10, verbose_name='OBP')),
                ('slugging_percentage', models.CharField(default='---', max_length=10, verbose_name='SLG')),
                ('on_base_plus_slugging', models.CharField(default='---', help_text='On-Base Plus Slugging\nCombined rate of OBP and SLG.\nOBP+SLG', max_length=10, verbose_name='OPS')),
                ('reached_on_error', models.IntegerField(blank=True, default=0, null=True)),
                ('fielders_choice', models.IntegerField(blank=True, default=0, null=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.game')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.playerseason')),
                ('team_stats', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.teamgamestats')),
            ],
            options={
                'verbose_name': "Hitter's Game Stats",
                'verbose_name_plural': "Hitter's Game Stats",
            },
        ),
    ]
