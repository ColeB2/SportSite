from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.urls import reverse

from taggit.managers import TaggableManager
from random import randint
from league.models import League


# Create your models here.
def unique_slug(obj_instance, obj_slug=None):
    """
    A function to calculate a unique slug for for instance. Assumes instance
    contained both a title field and slug field. Works by checking if slug is
    provided, if not, creates one, then checks if it exists. If it does, it adds
    a random int from 1-10000 to the end and checks it again.
    Based of code @:
    https://www.codingforentrepreneurs.com/blog/a-unique-slug-generator-for-django/.
    """
    if obj_slug:
        slug = obj_slug
    else:
        slug = slugify(obj_instance.title)

    obj_class = obj_instance.__class__
    queryset_exists = obj_class.objects.filter(slug=slug).exists()

    if queryset_exists:
        if obj_class.objects.get(slug=slug) == obj_instance:
            return slug
        else:
            new_slug = f"{slug}-{randint(1,10000)}"
            return unique_slug(obj_instance, obj_slug=new_slug)
    return slug

class Article(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='article_images', default='article_images/baseballplaceholder2.png')
    image_description = models.CharField(max_length=200, null=True, blank=True)
    date_posted = models.DateField(default=now)
    author = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, unique=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_abosulte_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.slug = unique_slug(self, self.slug)
        super(Article, self).save(*args, **kwargs)

