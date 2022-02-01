from django.test import TestCase
from league.models import Player, PlayerSeason, Season, SeasonStage, League
from league.models import PlayerSeason

# Create your tests here.
class LeagueTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.create(name="Test League", admin="Test User")
