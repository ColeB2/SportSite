# Generated by Django 4.0.1 on 2022-02-07 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0029_alter_season_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='location',
            field=models.CharField(blank=True, help_text='Defaults to home team.', max_length=50, null=True),
        ),
    ]
