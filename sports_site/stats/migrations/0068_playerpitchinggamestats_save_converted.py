# Generated by Django 3.1.7 on 2021-07-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0067_auto_20210708_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerpitchinggamestats',
            name='save_converted',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='SV'),
        ),
    ]
