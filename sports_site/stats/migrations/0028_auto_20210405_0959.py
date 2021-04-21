# Generated by Django 3.1.7 on 2021-04-05 14:59

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0027_auto_20210405_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='player',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='game', chained_model_field='season__season', null=True, on_delete=django.db.models.deletion.CASCADE, show_all=True, to='stats.playerseason'),
        ),
    ]
