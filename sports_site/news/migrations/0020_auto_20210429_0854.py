# Generated by Django 3.1.7 on 2021-04-29 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_auto_20210429_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
