# Generated by Django 3.1.7 on 2021-03-17 11:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_article_image_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date',
        ),
        migrations.AddField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 17, 11, 48, 29, 838968, tzinfo=utc)),
        ),
    ]
