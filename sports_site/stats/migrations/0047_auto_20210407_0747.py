# Generated by Django 3.1.7 on 2021-04-07 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0046_auto_20210407_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamgamestats',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.teamseason'),
        ),
    ]
