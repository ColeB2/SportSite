# Generated by Django 4.0.1 on 2022-05-25 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0032_alter_roster_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='abbreviation',
            field=models.SlugField(blank=True, max_length=4, null=True),
        ),
    ]
