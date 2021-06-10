# Generated by Django 3.1.7 on 2021-06-10 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0017_auto_20210531_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='final_score',
        ),
        migrations.AddField(
            model_name='game',
            name='away_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='home_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
