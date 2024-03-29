# Generated by Django 3.1.7 on 2021-04-05 13:19

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_auto_20210405_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerhittinggamestats',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.seasonstage'),
        ),
        migrations.AlterField(
            model_name='playerhittinggamestats',
            name='player',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='season', chained_model_field='season', null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.playerseason'),
        ),
    ]
