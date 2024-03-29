# Generated by Django 3.1.7 on 2021-07-08 11:37

from django.db import migrations, models
import stats.validators


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0064_auto_20210707_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerpitchinggamestats',
            name='average',
            field=models.FloatField(blank=True, null=True, verbose_name='AVG'),
        ),
        migrations.AlterField(
            model_name='playerpitchinggamestats',
            name='innings_pitched',
            field=models.FloatField(blank=True, default=0, help_text='Innings Pitched\nThe number of putouts recorded while the pitcher was on the mound divided by 3.\n.1 - 1 out/.2 - 2 outs.', null=True, validators=[stats.validators.validate_innings_pitched], verbose_name='IP'),
        ),
    ]
