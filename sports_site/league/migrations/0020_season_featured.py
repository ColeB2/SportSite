# Generated by Django 3.1.7 on 2021-07-12 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0019_auto_20210621_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='featured',
            field=models.BooleanField(default=True, null=True, verbose_name='Featured'),
        ),
    ]