from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse

from taggit.managers import TaggableManager


# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='article_images', default='article_images/baseballplaceholder2.png')
    image_description = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateField(default=now)
    author = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.headline

    def get_abosulte_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if Article.objects.filter(headline=self.headline).exists():
            self.slug = slugify(self.headline) + '-' + str(len(Article.objects.filter(headline=self.headline)))
        else:
            self.slug = slugify(self.headline)
        super(Article, self).save(*args, **kwargs)

