# Generated by Django 3.1.7 on 2021-03-23 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_remove_article_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(default='placeholder.png', upload_to='article_images'),
        ),
        migrations.AddField(
            model_name='article',
            name='image_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
