# Generated by Django 3.1.7 on 2021-04-09 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0052_auto_20210409_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamgamestats',
            name='roster',
        ),
        migrations.AlterField(
            model_name='playerseason',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.teamseason'),
        ),
        migrations.DeleteModel(
            name='Roster',
        ),
    ]
