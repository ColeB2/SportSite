# Generated by Django 3.1.7 on 2021-04-06 11:53

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0034_auto_20210406_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamgamestats',
            name='game',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='season', chained_model_field='season', null=True, on_delete=django.db.models.deletion.CASCADE, to='stats.game'),
        ),
    ]
