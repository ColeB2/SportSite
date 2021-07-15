# Generated by Django 3.1.7 on 2021-06-24 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0019_auto_20210621_0647'),
        ('stats', '0062_auto_20210622_0630'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playerpitchinggamestats',
            options={'verbose_name': "Pitching's Game Stats", 'verbose_name_plural': "Pitcher's Game Stats"},
        ),
        migrations.RemoveField(
            model_name='playerpitchinggamestats',
            name='average',
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='league.playerseason'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='league.seasonstage'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='team_stats',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.teamgamestats'),
        ),
    ]