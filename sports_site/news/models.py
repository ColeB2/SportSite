from django.db import models
from django.utils.timezone import now

# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    #TODO implement image, upload, and display
    image = models.ImageField(upload_to='article_images', default='article_images/baseballplaceholder2.png')
    image_description = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateField(default=now)
    author = models.CharField(max_length=30, null=True, blank=True)

