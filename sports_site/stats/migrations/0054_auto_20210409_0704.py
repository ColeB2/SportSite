# Generated by Django 3.1.7 on 2021-04-09 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0053_auto_20210409_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerseason',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.seasonstage'),
        ),
    ]
