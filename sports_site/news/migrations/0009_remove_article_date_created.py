# Generated by Django 3.1.7 on 2021-03-22 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20210322_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date_created',
        ),
    ]
