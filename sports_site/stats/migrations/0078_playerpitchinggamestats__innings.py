# Generated by Django 3.1.7 on 2021-10-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0077_auto_20211007_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerpitchinggamestats',
            name='_innings',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='IP'),
        ),
    ]
