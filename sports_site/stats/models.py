from django.db import models
from django.utils.timezone import now

# Create your models here.
SSN = {'R': 'Regular Season', 'P': 'Postseason', 'Pre':'Preseason'}
REGULAR = 'R'
POST = 'P'
PRE = 'Pre'

SEASON_TYPE = [
    (REGULAR, 'Regular Season'),
    (POST, 'Postseason'),
    (PRE, 'Preseason'),
]

class League(models.Model):
    name = models.CharField(max_length=100, null=False, default="League Name Here")

class Season(models.Model):
    year = models.CharField(max_length=10, null=False, default=now().year, help_text="Year in YYYY format, ie 2020")
    type = models.CharField(choices=SEASON_TYPE, max_length=20, null=True, default=REGULAR)


