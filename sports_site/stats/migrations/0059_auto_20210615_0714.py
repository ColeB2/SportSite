# Generated by Django 3.1.7 on 2021-06-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0058_auto_20210615_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='at_bats',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='AB'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='caught_stealing',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='CS'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='doubles',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='2B'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='fielders_choice',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='FC'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='hit_by_pitch',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='HBP'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='hits',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='H'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='homeruns',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='HR'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='plate_appearances',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='PA'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='reached_on_error',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='ROE'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='runs',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='R'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='runs_batted_in',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='RBI'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='sacrifice_bunts',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SAC'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='sacrifice_flies',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SF'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='singles',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='1B'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='stolen_bases',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SB'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='strikeouts',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SO'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='triples',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='3B'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='walks',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='BB'),
        ),
    ]
