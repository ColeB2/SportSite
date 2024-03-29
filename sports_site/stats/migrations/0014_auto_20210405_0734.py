# Generated by Django 3.1.7 on 2021-04-05 12:34

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0013_auto_20210405_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='player',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='game', chained_model_field='game', null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.playerseason'),
        ),
    ]
